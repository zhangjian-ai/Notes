## Pluggy

Pytest内置了诸多hook函数，使得用户可以使用这些hook在测试各个阶段完成自定义的测试需求。

在实际的测试需求中，往往同一个hook会被重写多次，这时，管理同一个hook的多个实现就要使用到pluggy（插件）模块。

最开始Pluggy是Pytest项目内部的一个模块，后来从Pytest中迁移出来，单独作为一个项目，Pytest也将Pluggy作为一个外部库使用。

下面通过一个示例，来逐步揭开Pluggy库的神秘面纱。

**演示代码**

```python
from pluggy import PluginManager, HookimplMarker, HookspecMarker

# PluginManager, HookimplMarker, HookspecMarker 的入参需要是相同的 project_name
hook_spec = HookspecMarker("demo")
hook_impl = HookimplMarker("demo")


class HookSpec:
    @hook_spec
    def calculate(self, a, b):
        pass


class HookImpl:
    @hook_impl
    def calculate(self, a, b):
        return a + b


pm = PluginManager("demo")
pm.add_hookspecs(HookSpec)
pm.register(HookImpl())  # 传入一个实例对象，这样使得方法被调用时无需传入self参数

# 切记在调用 hook 的时候参数必须是通过关键字的方式来传递
result = pm.hook.calculate(a=2, b=4)

print(result)  # [6]
```

**解析：**

1. `@hook_spec` 装饰器被调用时，本质上就是调用HookspecMarker的`__call__`方法，起作用是给被标记的function增加一个名为`project_name + '_spec'`，值为HookspecOpts实例的属性，HookspecOpts 是一个字典类，有了这个属性后，该func才能被`PluginManager.add_hookspecs`捕获，下面看看`HookspecMarker.__call__`方法源码

   ```python
       def __call__(self, function: _F | None = None, firstresult: bool = False, historic: bool = False, warn_on_impl: Warning | None = None ) -> _F | Callable[[_F], _F]:
       
           def setattr_hookspec_opts(func: _F) -> _F:
               if historic and firstresult:
                   raise ValueError("cannot have a historic firstresult hook")
              
             	# HookspecOpts说明：
               # firstresult  如果为True，则表示在执行当前hook_spec已经注册的所有hook_impl时，
               # 只要有hook_impl返回了非空结果，那么后面的hook_impl就不会再执行了
               # historic  如果为True，表示这个hook是需要保存call_history，注册新的hook_impl时需要进行回调
               # warn_on_impl If given, every implementation of this hook will trigger the given warning
               opts: HookspecOpts = {
                   "firstresult": firstresult,
                   "historic": historic,
                   "warn_on_impl": warn_on_impl,
               }
               setattr(func, self.project_name + "_spec", opts)  # 设置属性的
               return func
             
   				# 设置属性
           if function is not None:
               return setattr_hookspec_opts(function)
           else:
               return setattr_hookspec_opts
   ```

2. `@hook_impl` 装饰器被调用时，本质上就是调用HookspecMarker的`__call__`方法，起作用是给被标记的function增加一个名为`project_name + '_impl'`，值为HookimplOpts实例的属性，HookimplOpts 是一个字典类，有了这个属性后，该func才能被`PluginManager.register`捕获，下面看看`HookimplMarker.__call__`方法源码

   ```python
       def __call__(self, function: _F | None = None, hookwrapper: bool = False, optionalhook: bool = False, tryfirst: bool = False, trylast: bool = False, specname: str | None = None, wrapper: bool = False
                   ) -> _F | Callable[[_F], _F]:
   
           def setattr_hookimpl_opts(func: _F) -> _F:
           
           		# HookimplOpts 说明
             	# wrapper  如果为真，那么hook的实现函数中，必须包含yield。当执行到yield时，当前hook_impl会暂停执行，
               #          先把其他hook_impl执行完之后，在执行yield后面的代码，同时会将其他hook_impl的执行结果通过yield返回
               #          但返回的不再是Result对象
               # hookwrapper  和wrapper效果一样，只不过这是老版本用的参数，同时返回值封装为Result对象后再返回
               # optionalhook  可选地勾子，如果没有匹配到hook_spec也不会报错
               # tryfirst  在诸多hook_impl中最先执行
               # trylast   在诸多hook_impl中最后执行
               # specname  自定义的specname，如果有值，在查找hook_spec时，就不会使用当前func名了，直接使用specname
               opts: HookimplOpts = {
                   "wrapper": wrapper,
                   "hookwrapper": hookwrapper,
                   "optionalhook": optionalhook,
                   "tryfirst": tryfirst,
                   "trylast": trylast,
                   "specname": specname,
               }
               setattr(func, self.project_name + "_impl", opts)
               return func
   
           if function is None:
               return setattr_hookimpl_opts
           else:
               return setattr_hookimpl_opts(function)
   ```

3. `PluginManager.add_hookspecs` 是添加勾子规范的方法，根据func是否有`{projecy_name}_spec`属性，判断当前func是不是一个hook_spec（勾子函数规范），如果是就将其注入HookCaller，并保存到PluginManager实例的hook属性中

   ```python
       def add_hookspecs(self, module_or_class: _Namespace) -> None:  # 入参应该是一个模块或者类，其实只要是对象就可以
           """Add new hook specifications defined in the given ``module_or_class``.
   
           Functions are recognized as hook specifications if they have been
           decorated with a matching :class:`HookspecMarker`.
           """
           names = []
           for name in dir(module_or_class):  # dir把所有属性遍历出来
             	# 这里就是获取出前面@hook_spec给func注入的属性
               spec_opts = self.parse_hookspec_opts(module_or_class, name)  
               if spec_opts is not None:  # 没有 spec_opts 就没有后面的故事了
                 	# 判断当前hook中是否已经有这个func的HookCaller实例了
                   # HookCaller 将func封装进去，是所有已经注册的hook_spec的实现的调用对象
                   hc: HookCaller | None = getattr(self.hook, name, None)  
                   if hc is None:
                     	# 如果没有就创建HookCaller实例，保存到hook中，属性名就直接使用的func的名字
                       # 所以上面的示例中我们可以直接使用方法名实现了对hook的调用
                       hc = HookCaller(name, self._hookexec, module_or_class, spec_opts)
                       setattr(self.hook, name, hc)
                   else:
                       # 如果已经有了这个hc，那就把spec_opts设置到hc中，前提是这个hc中的spec_opts本来就没有，否则会报错
                       hc.set_specification(module_or_class, spec_opts)
                       for hookfunction in hc.get_hookimpls():
                           self._verify_hook(hc, hookfunction)
                   names.append(name)
   
           if not names:
               raise ValueError(f"did not find any {self.project_name!r} hooks in {module_or_class!r}")
      
     
     	# HookCaller.set_specification
       def set_specification(self, specmodule_or_class: _Namespace, spec_opts: HookspecOpts, ) -> None:
           # 不能重复配置hook_spec
           if self.spec is not None:
               raise ValueError(
                   f"Hook {self.spec.name!r} is already registered "
                   f"within namespace {self.spec.namespace}"
               )
           # 静态属性
           # HookSpec 中保存 函数所属的对象、函数名、spec_opts，并解析保存 函数、及函数入参
           self.spec = HookSpec(specmodule_or_class, self.name, spec_opts)
           # hook_spec中historic为True，表示可能需要用hook_impl的结果回调韩硕，先把_call_history设置为列表
           # 后续在调用 HookCaller.call_history方法时，会向列表添加历史回调记录
           if spec_opts.get("historic"):
               self._call_history = []
               
               
       @final
   		class HookSpec:
         __slots__ = ("namespace", "function", "name", "argnames", "kwargnames", "opts", "warn_on_impl")
   
         def __init__(self, namespace: _Namespace, name: str, opts: HookspecOpts) -> None:
             self.namespace = namespace
             self.function: Callable[..., object] = getattr(namespace, name)  # 解析函数
             self.name = name
             self.argnames, self.kwargnames = varnames(self.function)  # 解析入参
             self.opts = opts
             self.warn_on_impl = opts.get("warn_on_impl")
   ```

4. `PluginManager.register`是添加hook_impl的方法，根据当前func是否具有`{projecy_name}_impl`属性来确定当前func是不是一个hook_impl。同一个hook可以有多个hook_impl，二者的关系是`1:N`。

   ```python
       # PluginManager.register  _Plugin 就是 object
       def register(self, plugin: _Plugin, name: str | None = None) -> str | None:
       		# plugin_name 获取到的是 object.__name__
           plugin_name = name or self.get_canonical_name(plugin)
   				
           # self._name2plugin: Final[dict[str, _Plugin]] = {}
           # self._name2plugin 是一个常亮字典，可以添加kv，但不允许修改
           # 这里判断当前对象是否已经存在
           if plugin_name in self._name2plugin:
               if self._name2plugin.get(plugin_name, -1) is None:
                   return None  # blocked plugin, return None to indicate no registration
               raise ValueError(
                   "Plugin name already registered: %s=%s\n%s"
                   % (plugin_name, plugin, self._name2plugin)
               )
   				
           # 上面根据名字判断，但有可能用户传入了 name，就不是使用的 object.__name__ 了
           # 这里再根据对象判断一次
           if plugin in self._name2plugin.values():
               raise ValueError(
                   "Plugin already registered under a different name: %s=%s\n%s"
                   % (plugin_name, plugin, self._name2plugin)
               )
   
           # 不存在就添加
           self._name2plugin[plugin_name] = plugin
   
           # register matching hook implementations of the plugin
           for name in dir(plugin):
             	# 拿到 @hook_impl 注入的属性
               hookimpl_opts = self.parse_hookimpl_opts(plugin, name)
               # 为空就没有故事了
               if hookimpl_opts is not None:
                 	# 这里把 hookimpl_opts 中缺失的属性都设置为默认值
                   normalize_hookimpl_opts(hookimpl_opts)
                   # 拿到 hook_impl 方法
                   method: _HookImplFunction[object] = getattr(plugin, name)
                   
                   # 静态属性
                   # 将相关信息封装到 HookImpl，内部同样解析了函数相关的入参并保存
                   hookimpl = HookImpl(plugin, plugin_name, method, hookimpl_opts)
                   
                   # 这里的name应该是一个 hook_spec 的名字，有限使用specname。
                   # specname使得 @hook_spec 和 @hook_impl 修饰的方法名字可以不一样
                   name = hookimpl_opts.get("specname") or name
                   # 取出 hc。hc实在上一步中注入到self.hook中的
                   hook: HookCaller | None = getattr(self.hook, name, None)
                   
                   # 如果没有事先添加hook_spec，这里就直接添加一次，此时的hc中的hook_spec就为空了
                   # 当使用@hook_spec时，就会把spec_opts给补充到hc中
                   if hook is None:
                       hook = HookCaller(name, self._hookexec)
                       setattr(self.hook, name, hook)
                   # 如果有hc，且也有hook_spec
                   elif hook.has_spec():
                     	# 验证 hook_impl 的合法性
                       self._verify_hook(hook, hookimpl)
                       # hook_spec中historic为True时，新的hook_impl要执行历史回调
                       hook._maybe_apply_history(hookimpl)
                   # 将hook_impl添加到hc中，最终hc调用时，调用的就是hook_impl
                   hook._add_hookimpl(hookimpl)
           return plugin_name
         
       # HookCaller._add_hookimpl  添加hook_impl的逻辑。控制各个hook_impl的调用关系  
       def _add_hookimpl(self, hookimpl: HookImpl) -> None:
           """Add an implementation to the callback chain."""
           
           # 这里的逻辑会把 所有带yield的hook_impl放到self._hookimpls的后半部分，
           # 即使该hook_impl中tryfirst为True也是如此，因为yield始终要等其他没有yield的函数先执行。
           # tryfirst为True，只能让本hook_impl在多个包含yield的hook_impl中先执行，而不是所有的hook_impl
           for i, method in enumerate(self._hookimpls):
             	# 这里找到self._hookimpls中第一个包含yield的hook_impl的位置
               if method.hookwrapper or method.wrapper:
                   splitpoint = i
                   break
           # for 正常遍历完会走这里
           else:
               splitpoint = len(self._hookimpls)
               
           # 如果当前的hook_impl也包含yield，那么insert的区间就是
           # self._hookimpls中第一个包含yield的hook_impl的位置，到列表的末尾
           if hookimpl.hookwrapper or hookimpl.wrapper:
               start, end = splitpoint, len(self._hookimpls)
           # 同理不包含yield的hook_impl插入区间就是从0到第一个包含yield的hook_impl的位置
           else:
               start, end = 0, splitpoint
   				
           # 调用顺序遵循 LIFO 后进先出的原则
           # 所以 trylast时，insert到列表开头；tryfirst时，insert到列表最后
           if hookimpl.trylast:
               self._hookimpls.insert(start, hookimpl)
           elif hookimpl.tryfirst:
               self._hookimpls.insert(end, hookimpl)
           else:
               # 找到最后一个不是tryfirst的函数，放前面
               # 除开tryfirst，本次添加的hook_impl将会比先添加的hook_impl先执行
               i = end - 1
               while i >= start and self._hookimpls[i].tryfirst:
                   i -= 1
               self._hookimpls.insert(i + 1, hookimpl)
               
               
       @final
       class HookImpl:
           """A hook implementation in a :class:`HookCaller`."""
           __slots__ = ("function","argnames","kwargnames","plugin","opts","plugin_name","wrapper",
               "hookwrapper","optionalhook","tryfirst","trylast")
   
           def __init__(self, plugin: _Plugin, plugin_name: str, function: _HookImplFunction[object],
               hook_impl_opts: HookimplOpts) -> None:
             
               self.function: Final = function
               
               # 解析位置参数和关键词参数
               argnames, kwargnames = varnames(self.function)
               self.argnames: Final = argnames
               self.kwargnames: Final = kwargnames
               
               self.plugin: Final = plugin
               self.opts: Final = hook_impl_opts
               self.plugin_name: Final = plugin_name
               self.wrapper: Final = hook_impl_opts["wrapper"]
               self.hookwrapper: Final = hook_impl_opts["hookwrapper"]
               self.optionalhook: Final = hook_impl_opts["optionalhook"]
               self.tryfirst: Final = hook_impl_opts["tryfirst"]
               self.trylast: Final = hook_impl_opts["trylast"]
   
           def __repr__(self) -> str:
               return f"<HookImpl plugin_name={self.plugin_name!r}, plugin={self.plugin!r}>"
       
       # HookCaller._maybe_apply_history
       # 使用当前hook_impl返回值，把所有的回调函数都调用一遍
       def _maybe_apply_history(self, method: HookImpl) -> None:
           """Apply call history to a new hookimpl if it is marked as historic."""
           if self.is_historic():
               assert self._call_history is not None
               # self._call_history 中的值，是在调用 HookCaller.call_history方法时添加的，每掉一次记录一组
               # self._call_history 中保存一个二元tuple，0索引存放 hook_impl的形参，1索引存放回调函数
               for kwargs, result_callback in self._call_history:
                   res = self._hookexec(self.name, [method], kwargs, False)
                   if res and result_callback is not None:
                       # XXX: remember firstresult isn't compat with historic
                       assert isinstance(res, list)
                       result_callback(res[0])
   ```

5. `pm.hook.calculate`是hook调用的过程。`PluginManager`中的`hook`属性是一个静态实例，允许添加不允许修改，如果属性只是一个对象，对象内部是可以修改的，只要内存地址不变。

   前面的步骤中，往hook中注入了 key为方法名、value为HookCaller实例属性，这个HookCaller中包含了我们 hook名字、hookexec、hook所在的对象（module_or_class）、spec_opts 信息。

   其中：

   1. hookexec 是来自 PluginManager 中的一个属性，是执行 函数/方法 调用的关键；
   2. 通过 hook.方法名() 方式调用时，实际上调用的是 HookCaller 中的 `__call__` 方法

   

   根据调用顺序，先看`HookCaller.__call__`逻辑：

   ```python
       def __call__(self, **kwargs: object) -> Any:  # 这里就是为什么调用时，只接受关键字参数的原因
           # 如果hook_spec中historic是True，那么将不允许直接调用函数，要使用 hook.call_historic 方法
         	assert (
               not self.is_historic()
           ), "Cannot directly call a historic hook - use call_historic instead."
           # 检查参数都传入了
           self._verify_all_args_are_provided(kwargs)
           firstresult = self.spec.opts.get("firstresult", False) if self.spec else False
           # 传入 hook名称（函数名）、所有hook_impl、形参、firstresult，按顺序执行hook_impl
           # Copy because plugins may register other plugins during iteration (#438).
           return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
   ```

   

   hookexec逻辑：

   ```python
   class PluginManager:
       def __init__(self, project_name: str) -> None:
           self.project_name: Final = project_name
           self._name2plugin: Final[dict[str, _Plugin]] = {}
           self._plugin_distinfo: Final[list[tuple[_Plugin, DistFacade]]] = []
           self.hook: Final = HookRelay()
           self.trace: Final[_tracing.TagTracerSub] = _tracing.TagTracer().get("pluginmanage")
           # 3. 实际调用 _multicall
           self._inner_hookexec = _multicall
   		
       # 1. 创建HookCaller实例时，传入的就是这个方法
       def _hookexec(self, hook_name: str, methods: Sequence[HookImpl], kwargs: Mapping[str, object],
           firstresult: bool) -> object | list[object]:
           # 2. 内部调用 _inner_hookexec
           return self._inner_hookexec(hook_name, methods, kwargs, firstresult)
   ```

   ```python
   # caller_kwargs 是Mapping类型，可以理解为限制了键值类型的字典
   def _multicall(hook_name: str, hook_impls: Sequence[HookImpl], caller_kwargs: Mapping[str, object],
       firstresult: bool) -> object | list[object]:
       """Execute a call into multiple python functions/methods and return the
       result(s).
   
       ``caller_kwargs`` comes from HookCaller.__call__().
       """
       __tracebackhide__ = True
       results: list[object] = []
       exception = None
       only_new_style_wrappers = True
       try:  # run impl and wrapper setup functions in a loop
           teardowns: list[Teardown] = []
           try:
             	# 倒序遍历每个hook_impl，LIFO 后进先出原则
               for hook_impl in reversed(hook_impls):
                 	# 获取入参
                   try:
                       args = [caller_kwargs[argname] for argname in hook_impl.argnames]
                   except KeyError:
                       for argname in hook_impl.argnames:
                           if argname not in caller_kwargs:
                               raise HookCallError(f"hook call must provide argument {argname!r}")
   								
                   # 处理hook_impl中有yield的场景，这里兼容新老版本的参数 hookwrapper、wraper，都表示有yield
                   if hook_impl.hookwrapper:
                       only_new_style_wrappers = False
                       try:
                           # 调用函数，此时返回的是一个生成器
                           res = hook_impl.function(*args)
                           # 检查一下res是不是Generator，返回值仍然是res本身
                           wrapper_gen = cast(Generator[None, Result[object], None], res)
                           # 迭代一下，其实就是执行 yield 前面的代码
                           next(wrapper_gen)
                           # 放入teardown，让其他的hook_impl先执行
                           teardowns.append((wrapper_gen, hook_impl))
                       except StopIteration:
                           _raise_wrapfail(wrapper_gen, "did not yield")
                   elif hook_impl.wrapper:
                       try:
                           res = hook_impl.function(*args)
                           function_gen = cast(Generator[None, object, object], res)
                           next(function_gen)
                           # 同 hookwrapper 的逻辑，这里放入teardown的只有生成器
                           teardowns.append(function_gen)
                       except StopIteration:
                           _raise_wrapfail(function_gen, "did not yield")
                   else:
                     	# 普通 hook_impl的执行
                       res = hook_impl.function(*args)
                       if res is not None:
                         	# 保存结果
                           results.append(res)
                           # 如果当前hook_spec中firstresult为True，那么后面的hook_impl就不再执行
                           if firstresult:
                               break
           except BaseException as exc:
               exception = exc
       finally:
           # 如果hook_impl使用wrapper参数，那么通过yield返回的就不再是Result
           if only_new_style_wrappers:
             	# hook_spec 中 firstresult 为True时，直接返回第一个结果，否则返回结果列表
               if firstresult:
                   result = results[0] if results else None
               else:
                   result = results
   
               # 倒序执行 yield 后的代码，即先放入到 teardowns 中的Generater会后执行
               # 这样就能保证先注册的hook_impl对res的处理结果，可以被后注册的hook_impl使用到
               for teardown in reversed(teardowns):
                   try:
                       if exception is not None:
                           teardown.throw(exception)  # type: ignore[union-attr]
                       else:
                         	# 生成器通信，将结果返回到Genetater中
                           # 即 result = yield 
                           teardown.send(result)
                   except StopIteration as si:
                       result = si.value
                       exception = None
                       continue
                   except BaseException as e:
                       exception = e
                       continue
                   _raise_wrapfail(teardown, "has second yield")  # type: ignore[arg-type]
   
               if exception is not None:
                   raise exception.with_traceback(exception.__traceback__)
               else:
                   return result
   
           # 兼容处理 hookwrapper，将结果封装为Result对象，其他逻辑同上
           else:
               if firstresult:  # first result hooks return a single value
                   outcome: Result[object | list[object]] = Result(
                       results[0] if results else None, exception
                   )
               else:
                   outcome = Result(results, exception)
   
               for teardown in reversed(teardowns):
                   if isinstance(teardown, tuple):
                       try:
                         	# hookwrapper 逻辑下，放入到teardowns里面的是一个元祖（Generater, hook_impl）
                           teardown[0].send(outcome)
                       except StopIteration:
                           pass
                       except BaseException as e:
                           _warn_teardown_exception(hook_name, teardown[1], e)
                           raise
                       else:
                           _raise_wrapfail(teardown[0], "has second yield")
                   else:
                       try:
                           if outcome._exception is not None:
                               teardown.throw(outcome._exception)
                           else:
                               teardown.send(outcome._result)
                           teardown.close()
                       except StopIteration as si:
                           outcome.force_result(si.value)
                           continue
                       except BaseException as e:
                           outcome.force_exception(e)
                           continue
                       _raise_wrapfail(teardown, "has second yield")
   
               return outcome.get_result()
   ```




## PytestPluginManager

在Pytest中，实现了一个继承`pluggy.PluginManager`的子类`PytestPluginManager`并将诸多hook添加到了该类的实例中。下面从`pytest._jb_pytest_runner.py` 出发，梳理一下hook生效的流程。

1. `pytest._jb_pytest_runner.py`

   ```python
   # coding=utf-8
   import sys
   
   import pytest
   from _pytest.config import get_plugin_manager
   
   from pkg_resources import iter_entry_points
   
   from _jb_runner_tools import jb_patch_separator, jb_doc_args, JB_DISABLE_BUFFERING, start_protocol, parse_arguments, \
       set_parallel_mode
   from teamcity import pytest_plugin
   
   if __name__ == '__main__':
       path, targets, additional_args = parse_arguments()
       sys.argv += additional_args
       joined_targets = jb_patch_separator(targets, fs_glue="/", python_glue="::", fs_to_python_glue=".py::")
       joined_targets = [t + ".py" if ":" not in t else t for t in joined_targets]
       sys.argv += [path] if path else joined_targets
   
       plugins_to_load = []
       if not get_plugin_manager().hasplugin("pytest-teamcity"):
           if "pytest-teamcity" not in map(lambda e: e.name, iter_entry_points(group='pytest11', name=None)):
               plugins_to_load.append(pytest_plugin)
   
       args = sys.argv[1:]
       if JB_DISABLE_BUFFERING and "-s" not in args:
           args += ["-s"]
   
       jb_doc_args("pytest", args)
   
       class Plugin:
           @staticmethod
           def pytest_configure(config):
               if getattr(config.option, "numprocesses", None):
                   set_parallel_mode()
               start_protocol()
   
   		# 执行入口
       sys.exit(pytest.main(args, plugins_to_load + [Plugin]))
   ```

2. `main`

   ```python
   def main(args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
            plugins: Optional[Sequence[Union[str, _PluggyPlugin]]] = None) -> Union[int, ExitCode]:
       """
       Perform an in-process test run.
   
       :param args:
           List of command line arguments. If `None` or not given, defaults to reading
           arguments directly from the process command line (:data:`sys.argv`).
       :param plugins: 
       		List of plugin objects to be auto-registered during initialization.
   
       :returns: An exit code.
       """ 
       try:
           try:
             	# 1. config 初始化的过程
               config = _prepareconfig(args, plugins)
           except ConftestImportFailure as e:
               exc_info = ExceptionInfo.from_exception(e.cause)
               tw = TerminalWriter(sys.stderr)
               tw.line(f"ImportError while loading conftest '{e.path}'.", red=True)
               exc_info.traceback = exc_info.traceback.filter(
                   filter_traceback_for_conftest_import_failure
               )
               exc_repr = (
                   exc_info.getrepr(style="short", chain=False)
                   if exc_info.traceback
                   else exc_info.exconly()
               )
               formatted_tb = str(exc_repr)
               for line in formatted_tb.splitlines():
                   tw.line(line.rstrip(), red=True)
               return ExitCode.USAGE_ERROR
           else:
               try:
                 	# 2. 测试进程核心逻辑
                   ret: Union[ExitCode, int] = config.hook.pytest_cmdline_main(
                       config=config
                   )
                   try:
                       return ExitCode(ret)
                   except ValueError:
                       return ret
               finally:
                   config._ensure_unconfigure()
       except UsageError as e:
           tw = TerminalWriter(sys.stderr)
           for msg in e.args:
               tw.line(f"ERROR: {msg}\n", red=True)
           return ExitCode.USAGE_ERROR
   ```

3. `config`对象的创建过程

   - `_prepareconfig`

     ```python
     def _prepareconfig(args: Optional[Union[List[str], "os.PathLike[str]"]] = None,
                        plugins: Optional[Sequence[Union[str, _PluggyPlugin]]] = None) -> "Config":
       	# 没有参数就自己拿
         if args is None:
             args = sys.argv[1:]
         elif isinstance(args, os.PathLike):
             args = [os.fspath(args)]
         elif not isinstance(args, list):
             msg = (  # type:ignore[unreachable]
                 "`args` parameter expected to be a list of strings, got: {!r} (type: {})"
             )
             raise TypeError(msg.format(args, type(args)))
     		
         # 创建config对象
         config = get_config(args, plugins)
         pluginmanager = config.pluginmanager
         
         # 下面的逻辑是添加一些特殊的插件，不用关心
         try:
             if plugins:
                 for plugin in plugins:
                     if isinstance(plugin, str):
                         pluginmanager.consider_pluginarg(plugin)
                     else:
                         pluginmanager.register(plugin)
             # pytest_cmdline_parse 返回值仍然是config
             config = pluginmanager.hook.pytest_cmdline_parse(
                 pluginmanager=pluginmanager, args=args
             )
             return config
         except BaseException:
             config._ensure_unconfigure()
             raise
     ```

   - 跟进`get_config`，里面三个步骤要逐个分析

     ```python
     def get_config(args: Optional[List[str]] = None,
                    plugins: Optional[Sequence[Union[str, _PluggyPlugin]]] = None) -> "Config":
         # 1.插件管理对象
         pluginmanager = PytestPluginManager()
         
         # 2.创建config
         config = Config(
             pluginmanager,
             invocation_params=Config.InvocationParams(
                 args=args or (),
                 plugins=plugins,
                 dir=Path.cwd(),
             ),
         )
     
         if args is not None:
             # Handle any "-p no:plugin" args.
             pluginmanager.consider_preparse(args, exclude_only=True)
     		
         # 3.这里就是注册pytest框架所有的内置hook_impl
         #   default_plugins 是实现整理好顺序的需要导入的内置模块
         for spec in default_plugins:
             pluginmanager.import_plugin(spec)
     
         return config
     ```

   - 第一步看`PytestPluginManager`实例化的过程，这个过程中完成 add_hookspec

     ```python
     @final
     class PytestPluginManager(PluginManager):
     
         def __init__(self) -> None:
             import _pytest.assertion
     
             super().__init__("pytest")
     
             self._conftest_plugins: Set[types.ModuleType] = set()
             self._dirpath2confmods: Dict[Path, List[types.ModuleType]] = {}
             self._confcutdir: Optional[Path] = None
             self._noconftest = False
             self._get_directory = lru_cache(256)(_get_directory)
     
             self.skipped_plugins: List[Tuple[str, str]] = []
     				
             # 这里完成了add_hookspec
             # _pytest.hookspec 是一个模块，里面定义了内建的所有hook，并使用@hookspec标记
             # 有部分未做标记，将不能使用HookCaller调用
             self.add_hookspecs(_pytest.hookspec)
             # 将自己内部的hook_impl注册
             self.register(self)
     ```

     ```python
     @final
     class PytestPluginManager(PluginManager):
     
         def __init__(self) -> None:
             import _pytest.assertion
     
             super().__init__("pytest")
     
             self._conftest_plugins: Set[types.ModuleType] = set()
             self._dirpath2confmods: Dict[Path, List[types.ModuleType]] = {}
             self._confcutdir: Optional[Path] = None
             self._noconftest = False
             self._get_directory = lru_cache(256)(_get_directory)
     
             self.skipped_plugins: List[Tuple[str, str]] = []
     				
             # 这里完成了add_hookspec
             # _pytest.hookspec 是一个模块，里面定义了内建的所有hook，并使用@hookspec标记
             # 有部分未做标记，将会被提供默认的spec_opts来完成add
             self.add_hookspecs(_pytest.hookspec)
             # 将自己内部的hook_impl注册
             self.register(self)
     ```

   - 第二步看`config`实例化

     ```python
     @final
     class Config:
       
         def __init__(self, 
                      pluginmanager: PytestPluginManager, *,
                      invocation_params: Optional[InvocationParams] = None ) -> None:
           
             from .argparsing import FILE_OR_DIR
             from .argparsing import Parser
     
             if invocation_params is None:
                 invocation_params = self.InvocationParams(
                     args=(), plugins=None, dir=Path.cwd()
                 )
     				# option就是保存命令行参数的对象
             # Namespace 就是一个用于存储attr的简单类型
             self.option = argparse.Namespace()
     				
             # Config内部类InvocationParams的实例，保存了args、plugins、项目路径
             self.invocation_params = invocation_params
     
             _a = FILE_OR_DIR
             self._parser = Parser(
                 usage=f"%(prog)s [options] [{_a}] [{_a}] [...]",
                 processopt=self._processopt,
                 _ispytest=True,
             )
             
             # 前面创建的插件管理对象
             self.pluginmanager = pluginmanager
     				
             # 一个存储键值的容器，内部维护的是一个字典
             self.stash = Stash()
             self._store = self.stash
     
             self.trace = self.pluginmanager.trace.root.get("config")
             
             # hook对象，简单理解就是pluginmanager.hook
             self.hook: pluggy.HookRelay = PathAwareHookProxy(self.pluginmanager.hook)
             
             self._inicache: Dict[str, Any] = {}
             self._override_ini: Sequence[str] = ()
             self._opt2dest: Dict[str, str] = {}
             self._cleanup: List[Callable[[], None]] = []
             
             # 将config对象以 'pytestconfig'的名字注册到插件中
             self.pluginmanager.register(self, "pytestconfig")
             
             self._configured = False
             
             # 这里通过回访历史的方式，实现了命令行参数的添加
             # 但其实这里并没有传入 回调函数，因为 pytest_addoption 并没有返回值
             self.hook.pytest_addoption.call_historic(
                 kwargs=dict(parser=self._parser, pluginmanager=self.pluginmanager)
             )
             self.args_source = Config.ArgsSource.ARGS
             self.args: List[str] = []
     
             if TYPE_CHECKING:
                 from _pytest.cacheprovider import Cache
     
                 self.cache: Optional[Cache] = None
     ```

     ```python
       # HookCaller.call_historic
       def call_historic(
             self,
             result_callback: Callable[[Any], None] | None = None,  # 回调函数
             kwargs: Mapping[str, object] | None = None,  # hook_impl 的入参
         ) -> None:
             
           	# 在介绍Pluggy时，
             assert self._call_history is not None
             kwargs = kwargs or {}
             self._verify_all_args_are_provided(kwargs)
             
             # 添加回调记录
             self._call_history.append((kwargs, result_callback))
             
             # 用所有的hook_impl结果，回调result_callback。因此此时 firstresult 直接给 False
             res = self._hookexec(self.name, self._hookimpls.copy(), kwargs, False)
             if result_callback is None:
                 return
             # 使用回调函数，把所有hook_impl结果都调用一遍
             if isinstance(res, list):
                 for x in res:
                     result_callback(x)
     ```

   - 第三步看`pluginmanager.import_plugin`，导入默认插件。

     ```python
         def import_plugin(self, modname: str, consider_entry_points: bool = False) -> None:
             """Import a plugin with ``modname``.
     
             If ``consider_entry_points`` is True, entry point names are also
             considered to find a plugin.
             """
             assert isinstance(modname, str), ("module name as text required, got %r" % modname)
             
             if self.is_blocked(modname) or self.get_plugin(modname) is not None:
                 return
     				
             # 导入的hook_spec的名字，这里其实就是 _pytest库内的模块
             # _pytest库 是pytest依赖库，pytest目前仅作为调用入口，所有逻辑、参数定义都在_pytest中
             # builtin_plugins 中模块的顺序是有严格要求的，控制这同一hook_spec的多个hook_impl的调用顺序
             importspec = "_pytest." + modname if modname in builtin_plugins else modname
             # 下面这一句，啥也没干
             self.rewrite_hook.mark_rewrite(importspec)
     
             if consider_entry_points:
                 loaded = self.load_setuptools_entrypoints("pytest11", name=modname)
                 if loaded:
                     return
     
             try:
               	# 模块导入
                 __import__(importspec)
             except ImportError as e:
                 raise ImportError(
                     f'Error importing plugin "{modname}": {e.args[0]}'
                 ).with_traceback(e.__traceback__) from e
     
             except Skipped as e:
                 self.skipped_plugins.append((modname, e.msg or ""))
             else:
               	# 拿到模块，并注册到plugginmanager
                 # 到这里就完成了pytest内建勾子的add_hookspec及register
                 mod = sys.modules[importspec]
                 self.register(mod, modname)
     ```

4. `pytest_cmdline_main` 内建钩子函数的调用。pytest核心的逻辑就在其中。`pytest_cmdline_main`在`_pytest`多个模块中都有实现，分别处理着前置后置的一些工作，其中调用主流程的hook_impl在`_pytest.main.py`文件中。

   ```python
   # 这里并没有使用 @hookimpl，但仍然被收集到 pytestpluginmanager.hook.pytest_cmdline_main._hookimpls中。
   # 下一步分析原因
   def pytest_cmdline_main(config: Config) -> Union[int, ExitCode]:
       return wrap_session(config, _main)
     
   def wrap_session(
       config: Config, doit: Callable[[Config, "Session"], Optional[Union[int, ExitCode]]]
   ) -> Union[int, ExitCode]:
       """Skeleton command line program."""
       session = Session.from_config(config)
       session.exitstatus = ExitCode.OK
       initstate = 0
       try:
           try:
               config._do_configure()
               initstate = 1
               config.hook.pytest_sessionstart(session=session)
               initstate = 2
               # 调用 _main
               session.exitstatus = doit(config, session) or 0
           except UsageError:
   						...
   
       finally:
           # Explicitly break reference cycle.
           excinfo = None  # type: ignore
           os.chdir(session.startpath)
           if initstate >= 2:
               try:
                   config.hook.pytest_sessionfinish(
                       session=session, exitstatus=session.exitstatus
                   )
               except exit.Exception as exc:
                   if exc.returncode is not None:
                       session.exitstatus = exc.returncode
                   sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
           config._ensure_unconfigure()
       return session.exitstatus
   
   def _main(config: Config, session: "Session") -> Optional[Union[int, ExitCode]]:
       """Default command line protocol for initialization, session,
       running tests and reporting."""
       config.hook.pytest_collection(session=session)
       config.hook.pytest_runtestloop(session=session)
   
       if session.testsfailed:
           return ExitCode.TESTS_FAILED
       elif session.testscollected == 0:
           return ExitCode.NO_TESTS_COLLECTED
       return None
   ```

5. 其实不仅`_pytest.main`模块，`_pytest`库里面很多模块里面的hook函数都没有使用`@hookimpl`，`hookspec`模块中有些hook甚至都没有使用`@hookspec`标记，但仍然被扫描到并正常调用。

   其原因就是 PytestPluginManager 重写了父类中两个解析 hookspec、hookimpl 的方法。

   ```python
   @final
   class PytestPluginManager(PluginManager):
   		# 初始化方法在前面已经看过
       def __init__(self) -> None:...
   
   
       def parse_hookimpl_opts(self, plugin: _PluggyPlugin, name: str) -> Optional[HookimplOpts]:
   				# 可以看到pytest中，限制了hook名字，必须是 pytest 开头的
           if not name.startswith("pytest_"):
               return None
            
           # 忽略 pytest_plugins 这个特殊函数
           if name == "pytest_plugins":
               return None
   				
           # 如果使用了 @hookimpl 将会拿到 impl_opts ，就直接返回了
           opts = super().parse_hookimpl_opts(plugin, name)
           if opts is not None:
               return opts
   				
           # 下面就是处理 impl_opts 为空时，返回默认 impl_opts
           method = getattr(plugin, name)
           if not inspect.isroutine(method):
               return None
           # 只要是没有被 @hookimpl 标记，且以 pytest_ 前缀开头的函数，都会给这样一个默认的 impl_opts
           # 使得该函数可以被收集到
           return _get_legacy_hook_marks(
               method, "impl", ("tryfirst", "trylast", "optionalhook", "hookwrapper"))
   
       def parse_hookspec_opts(self, module_or_class, name: str) -> Optional[HookspecOpts]:
           
           # 同样，在 add_hookspec 时，也会为 pytest 开头的未被 @hookspec 标记的函数返回默认的 spec_opts
           opts = super().parse_hookspec_opts(module_or_class, name)
           if opts is None:
               method = getattr(module_or_class, name)
               if name.startswith("pytest_"):
                   opts = _get_legacy_hook_marks(  # type: ignore[assignment]
                       method,
                       "spec",
                       ("firstresult", "historic"),
                   )
           return opts
   		
       def register(self, plugin: _PluggyPlugin, name: Optional[str] = None) -> Optional[str]:...
   ```

   



## xdist

xdist是pytest的一个三方插件库，由于实现分布式测试。同许多其他的pytest插件一样，pytest-xdist 在安装时通过将自身的入口文件添加到entry_points的 `pytest11` 组中，是在pytest在开始执行时，可以成功扫描到插件并运行其对应的hook。

再看一下`PytestPluginManager`中的入口文件，就可以发现pytest做了收集三方插件的动作。

```python
# coding=utf-8
import sys

import pytest
from _pytest.config import get_plugin_manager

from pkg_resources import iter_entry_points

from _jb_runner_tools import jb_patch_separator, jb_doc_args, JB_DISABLE_BUFFERING, start_protocol, parse_arguments, \
    set_parallel_mode
from teamcity import pytest_plugin

if __name__ == '__main__':
    path, targets, additional_args = parse_arguments()
    sys.argv += additional_args
    joined_targets = jb_patch_separator(targets, fs_glue="/", python_glue="::", fs_to_python_glue=".py::")
    joined_targets = [t + ".py" if ":" not in t else t for t in joined_targets]
    sys.argv += [path] if path else joined_targets
		
    # 就是这里通过获取entry_points中的pytest11组中的entry，拿到其他三方插件的入口文件
    plugins_to_load = []
    if not get_plugin_manager().hasplugin("pytest-teamcity"):
        if "pytest-teamcity" not in map(lambda e: e.name, iter_entry_points(group='pytest11', name=None)):
            plugins_to_load.append(pytest_plugin)

    args = sys.argv[1:]
    if JB_DISABLE_BUFFERING and "-s" not in args:
        args += ["-s"]

    jb_doc_args("pytest", args)

    class Plugin:
        @staticmethod
        def pytest_configure(config):
            if getattr(config.option, "numprocesses", None):
                set_parallel_mode()
            start_protocol()

		# 执行入口
    sys.exit(pytest.main(args, plugins_to_load + [Plugin]))
```



xdist是三方库中的热门库，分布式的执行可以大大节省测试的时间。下面从xdist入口来分析一下。

1. `xdist.plugin.py`   这个文件主要是通过pytest内置的hook完成一些必要的工作，比如 xdist命令行参数注册、xdist的hook注册，以及初始化工作。

   ```python
   # xdist.plugin.py
   
   # 注册命令行
   @pytest.hookimpl
   def pytest_addoption(parser):
       group = parser.getgroup("xdist", "distributed and subprocess testing")
       # 这是分布式执行时，开启的进程数
       group._addoption(
           "-n",
           "--numprocesses",
           dest="numprocesses",
           metavar="numprocesses",
           action="store",
           type=parse_numprocesses,
           help="Shortcut for '--dist=load --tx=NUM*popen'. With 'auto', attempt "
           "to detect physical CPU count. With 'logical', detect logical CPU "
           "count. If physical CPU count cannot be found, falls back to logical "
           "count. This will be 0 when used with --pdb.",
       )
       ...
       # 指定进程开启的方式，默认是 popen，在当前main进程下开启子进程来执行
       group.addoption(
           "--tx",
           dest="tx",
           action="append",
           default=[],
           metavar="xspec",
           help=(
               "add a test execution environment. some examples: "
               "--tx popen//python=python2.5 --tx socket=192.168.1.102:8888 "
               "--tx ssh=user@codespeak.net//chdir=testcache"
           ),
       )
   
   # 注册xdist独有的hook
   @pytest.hookimpl
   def pytest_addhooks(pluginmanager):
       from xdist import newhooks
   
       pluginmanager.add_hookspecs(newhooks)
       
   
   # 在其他pytest_configure执行完后，再执行xdist的
   @pytest.hookimpl(trylast=True)
   def pytest_configure(config):
       config_line = (
           "xdist_group: specify group for tests should run in same session."
           "in relation to one another. Provided by pytest-xdist."
       )
       config.addinivalue_line("markers", config_line)
   
       # Skip this plugin entirely when only doing collection.
       if config.getvalue("collectonly"):
           return
   
       # config.getoption("dist") 拿到的是分布式调度策略，命令行传入，后续再说取值
       if config.getoption("dist") != "no" and config.getoption("tx"):
           from xdist.dsession import DSession
   				
           # 创建分布式会话对象。DSession = distributed session
           session = DSession(config)
           
           # 把DSession中的hook_impl也给注册了
           config.pluginmanager.register(session, "dsession")
           tr = config.pluginmanager.getplugin("terminalreporter")
           if tr:
               tr.showfspath = False
               
       ...
   
    # 这个勾子要在其他hook_impl前面执行，这里指定了默认的并发执行方式
   @pytest.hookimpl(tryfirst=True)
   def pytest_cmdline_main(config):
       usepdb = config.getoption("usepdb", False)  # a core option
       if config.option.numprocesses in ("auto", "logical"):
           if usepdb:
               config.option.numprocesses = 0
               config.option.dist = "no"
           else:
               auto_num_cpus = config.hook.pytest_xdist_auto_num_workers(config=config)
               config.option.numprocesses = auto_num_cpus
   
       if config.option.numprocesses:
           if config.option.dist == "no":
               config.option.dist = "load"
           numprocesses = config.option.numprocesses
           if config.option.maxprocesses:
               numprocesses = min(numprocesses, config.option.maxprocesses)
           # 根据指定的进程数，配置 --tx 的值，列表长度表示开启worker的个数，”popen“表示使用子进程
           config.option.tx = ["popen"] * numprocesses
       if config.option.distload:
           config.option.dist = "load"
       val = config.getvalue
       if not val("collectonly") and val("dist") != "no" and usepdb:
           raise pytest.UsageError(
               "--pdb is incompatible with distributing tests; try using -n0 or -nauto."
           )  
   ```
   
   ```python
   # xdist.dsession.py
   
   class DSession:
     	# 下面就是说这是一个分布式会话类，从创建 NodeManager 实例开始
       # 然后各节点就可以通过一些事件发布实现通信，从而完成自动化的测试
       
       """A pytest plugin which runs a distributed test session
   
       At the beginning of the test session this creates a NodeManager
       instance which creates and starts all nodes.  Nodes then emit
       events processed in the pytest_runtestloop hook using the worker_*
       methods.
   
       Once a node is started it will automatically start running the
       pytest mainloop with some custom hooks.  This means a node
       automatically starts collecting tests.  Once tests are collected
       it will wait for instructions.
       """
   
       def __init__(self, config):...
       
       
       @pytest.hookimpl(trylast=True)
       def pytest_sessionstart(self, session):
           # 创建节点管理实例
           self.nodemanager = NodeManager(self.config)
           # 初始化节点，后面在 NodeManager类可看到实现细节
           # 传入一个队列put方法，用于保存event
           # >>>>> 注意，下面就是开启worker的逻辑，因此子进程开启是在 pytest_sessionstart 中完成的。
           # 最终拿到各个工作节点
           nodes = self.nodemanager.setup_nodes(putevent=self.queue.put)
           self._active_nodes.update(nodes)
           self._session = session
           
       @pytest.hookimpl(trylast=True)
       def pytest_xdist_make_scheduler(self, config, log):
         	"""
         	这是xdist自己的hook，返回一个调度类。master节点根据调度类的实现对用例进行分发
         	"""
           dist = config.getvalue("dist")  # 可以看到，命令行的取值，得是下面其中之一
           schedulers = {
               "each": EachScheduling,  # 每个worker都把所有用例执行一遍
               "load": LoadScheduling,  # 所有worker均分测试用例
               "loadscope": LoadScopeScheduling,  # 根据作用域调度，将同一个文件的用例调度到同一个worker
               "loadfile": LoadFileScheduling,  # 和上面一样的
               "loadgroup": LoadGroupScheduling,  # 用得少。根据名称规则来分。用例名包含了@符号，@后面部分就是group名
               "worksteal": WorkStealingScheduling,  # 就是执行的快的节点，会再被分配其他节点还没执行用例
           }
           return schedulers[dist](config, log)
         
       # 下面两个xidst hook 在NodeManager中用到
       # 这里就是记录了每个worker（Xspec 示例）的状态
       @pytest.hookimpl
       def pytest_xdist_setupnodes(self, specs) -> None:
           self._specs = specs
           for spec in specs:
               self.setstatus(spec, WorkerStatus.Created, tests_collected=0, show=False)
           self.setstatus(spec, WorkerStatus.Created, tests_collected=0, show=True)
           self.ensure_show_status()
   
       @pytest.hookimpl
       def pytest_xdist_newgateway(self, gateway) -> None:
           if self.config.option.verbose > 0:
               rinfo = gateway._rinfo()
               different_interpreter = rinfo.executable != sys.executable
               if different_interpreter:
                   version = "%s.%s.%s" % rinfo.version_info[:3]
                   self.rewrite(
                       f"[{gateway.id}] {rinfo.platform} Python {version} cwd: {rinfo.cwd}",
                       newline=True,
                   )
           self.setstatus(gateway.spec, WorkerStatus.Initialized, tests_collected=0)
   ```
   
   ```python
   # xdist.workermanage.py
   
   class NodeManager:
       EXIT_TIMEOUT = 10
       DEFAULT_IGNORES = [".*", "*.pyc", "*.pyo", "*~"]
   
       def __init__(self, config, specs=None, defaultchdir="pyexecnetcache") -> None:
         	# gateway group
           self.group = execnet.Group()
         ...
           # 介绍worker创建逻辑
           if specs is None:
             	# 构建 Xspec 示例，默认情况下仅仅是一个特定结构的示例，还没有实际意义的赋值
               specs = self._getxspecs()
           self.specs = []
           for spec in specs:
               if not isinstance(spec, execnet.XSpec):
                   spec = execnet.XSpec(spec)
               # 默认会满足这个条件
               if not spec.chdir and not spec.popen:
                   spec.chdir = defaultchdir  # 默认传参 pyexecnetcache
               # 这里给worker分配ID，就是 gw0 gw1 ...
               self.group.allocate_id(spec)
               self.specs.append(spec)
         
         ...
       
       # 使用 --tx 参数，构建了一个 Xspec实例的列表
       def _getxspecs(self):
           return [execnet.XSpec(x) for x in parse_spec_config(self.config)]
       
       # DSession 中调用这里
       def setup_nodes(self, putevent):
         	# 传入节点通信的配置并完成节点初始状态设置，把每个worker的id和对应状态做了记录
           self.config.hook.pytest_xdist_setupnodes(config=self.config, specs=self.specs)
           self.trace("setting up nodes")
           # 
           return [self.setup_node(spec, putevent) for spec in self.specs]
   
       def setup_node(self, spec, putevent):
         	# 创建通信网关，是一个 Gateway实例，Xspec实例会作为 gw的spec属性
           # 就是开启了一个子进程，这个网关代理了当前进程和子进程的通信
           gw = self.group.makegateway(spec)
           # 这里就是打印了一下 每个gw的信息，比如 id、运行的平台、python版本等
           self.config.hook.pytest_xdist_newgateway(gateway=gw)
           self.rsync_roots(gw)
           # 节点管理实例，再把 gw 收纳进去，再代理一层
           node = WorkerController(self, gw, self.config, putevent)
           gw.node = node  # keep the node alive
           node.setup()  # 往下看实现逻辑
           self.trace("started node %r" % node)
           return node
           ...
           
           
   class WorkerController:
       ENDMARK = -1
   
       class RemoteHook:
           @pytest.hookimpl(trylast=True)
           def pytest_xdist_getremotemodule(self):
               return xdist.remote  # 节点通信逻辑
   
       def __init__(self, nodemanager, gateway, config, putevent):
         	# xdist hook 注册
           config.pluginmanager.register(self.RemoteHook())
           self.nodemanager = nodemanager
           self.putevent = putevent
           self.gateway = gateway  # 网关
           self.config = config
           self.workerinput = {  # worker 信息，会下发到对应的worker并设置这些信息
               "workerid": gateway.id,
               "workercount": len(nodemanager.specs),
               "testrunuid": nodemanager.testrunuid,
               "mainargv": sys.argv,
           }
           self._down = False
           self._shutdown_sent = False
           self.log = Producer(f"workerctl-{gateway.id}", enabled=config.option.debug)
       
       
       def setup(self):
           self.log("setting up worker session")
           spec = self.gateway.spec
           if hasattr(self.config, "invocation_params"):
               args = [str(x) for x in self.config.invocation_params.args or ()]
               option_dict = {}
           else:
               args = self.config.args
               option_dict = vars(self.config.option)
           if not spec.popen or spec.chdir:
               args = make_reltoroot(self.nodemanager.roots, args)
           if spec.popen:
               name = "popen-%s" % self.gateway.id
               if hasattr(self.config, "_tmp_path_factory"):
                   basetemp = self.config._tmp_path_factory.getbasetemp()
                   option_dict["basetemp"] = str(basetemp / name)
           self.config.hook.pytest_configure_node(node=self)
   				
           # remote_module 就是需要让worker执行的脚本
           remote_module = self.config.hook.pytest_xdist_getremotemodule()
           # 使用代理的网关，让worker执行脚本。脚本中会接受当前进程send的信息
           self.channel = self.gateway.remote_exec(remote_module)
           
           change_sys_path = _sys_path if self.gateway.spec.popen else None
           
           # 这里将信息下发给worker
           self.channel.send((self.workerinput, args, option_dict, change_sys_path))
   
           if self.putevent:
               self.channel.setcallback(self.process_from_remote, endmarker=self.ENDMARK)
   ```
   
   ```python
   # xdist.remote.py
   
   # 一部分源码
   if __name__ == "__channelexec__":
       channel = channel  # type: ignore[name-defined] # noqa: F821
       
       # 这里worker阻塞，直到拿到master下发的信息
       workerinput, args, option_dict, change_sys_path = channel.receive()  # type: ignore[name-defined]
   
       if change_sys_path is None:
           importpath = os.getcwd()
           sys.path.insert(0, importpath)
           os.environ["PYTHONPATH"] = (
               importpath + os.pathsep + os.environ.get("PYTHONPATH", "")
           )
       else:
           sys.path = change_sys_path
   		
       # 环境变量
       os.environ["PYTEST_XDIST_TESTRUNUID"] = workerinput["testrunuid"]
       os.environ["PYTEST_XDIST_WORKER"] = workerinput["workerid"]
       os.environ["PYTEST_XDIST_WORKER_COUNT"] = str(workerinput["workercount"])
   
       if hasattr(Config, "InvocationParams"):
         	# worker当中的config，是pytest原生的Config实例，和master中的Config有区别，这里不会注册xdist-master的hook
           # 但是用户自定义的部分，一个不会少
           config = _prepareconfig(args, None)
       else:
           config = remote_initconfig(option_dict, args)
           config.args = args
   
       setup_config(config, option_dict.get("basetemp"))
       config._parser.prog = os.path.basename(workerinput["mainargv"][0])
       config.workerinput = workerinput  # type: ignore[attr-defined]
       config.workeroutput = {}  # type: ignore[attr-defined]
       
       # 创建worker交互实例，里面提供了诸多hook_impl，以完成主从的交互
       interactor = WorkerInteractor(config, channel)  # type: ignore[name-defined]
       config.hook.pytest_cmdline_main(config=config)
   ```
   
   ```python
   # xdist.remote.py
   
   class WorkerInteractor:
       def __init__(self, config, channel):
           self.config = config
           self.workerid = config.workerinput.get("workerid", "?")
           self.testrunuid = config.workerinput["testrunuid"]
           self.log = py.log.Producer("worker-%s" % self.workerid)
           if not config.option.debug:
               py.log.setconsumer(self.log._keywords, None)
           self.channel = channel
           
           # 注册hook_impl
           config.pluginmanager.register(self)
       
       ...
       
       # worker 执行用例的核心逻辑
       @pytest.hookimpl
       def pytest_runtestloop(self, session):
           self.log("entering main loop")
           torun = []
           
           # 要做什么动作，均由master通知，直到接收到 shutdown 信号
           # 因为 子进程 也完成了用例收集等动作，因此执行时拿到需要执行的用例在 items 中的索引即可
           while 1:
               try:
                   name, kwargs = self.channel.receive()
               except EOFError:
                   return True
               self.log("received command", name, kwargs)
               if name == "runtests":
                   torun.extend(kwargs["indices"])
               elif name == "runtests_all":
                   torun.extend(range(len(session.items)))
               self.log("items to run:", torun)
               # only run if we have an item and a next item
               while len(torun) >= 2:
                   self.run_one_test(torun)
               if name == "shutdown":
                   if torun:
                       self.run_one_test(torun)
                   break
           return True
   ```
   
   
   
   

## allure

Allure是一个开源的测试报告生成框架，提供了测试报告定制化功能，相较于 pytest-html插件 生成的html格式的测试报告，通过Allure生成的报告更加规范、清晰、美观。

pytest框架支持使用Allure生成测试报告，下面介绍pytest怎样结合Allure生成测试报告。

1. 安装 allure-pytest：

   ```shell
   pip install allure-pytest
   ```

2. 下载Allure，Allure依赖 jdk(1.8+) 。地址：https://github.com/allure-framework/allure2/releases

3. 代码演示使用方法：

   > 为了方便演示，示例代码使用手动标记用例的信息，在实际工程这样编写工作量巨大，且难维护。
   >
   > 通常推荐使用 `allure.dynamic` 实例，实现图动态添加用例信息

   ```python
   import os
   import allure
   import pytest
   
   @allure.step("登录获取token")
   def get_token():
       print("请求登录接口获取token")
   
   @allure.step("加入购物车")
   def add_to_shopping_trolley():
       print("请求加入购物车接口")
   
   @allure.step("查询我的购物车")
   def get_shopping_trolley_goods():
       print("请求查询我的购物车接口")
   
   @allure.step("清空购物车")
   def empty_shopping_trolley():
       print("请求清空购物车接口")
   
   @allure.step("下单")
   def place_order():
       print("请求下单接口")
   
   
   @allure.epic("xx在线购物平台接口测试")
   @allure.feature("购物车功能模块")
   class TestShoppingTrolley:
   
       @allure.story("商品加入购物车")
       @allure.title("正向用例--将库存数>0的商品加入购物车")
       @allure.description("校验库存数不为0的商品加入购物车是否正常")
       @allure.severity("critical")
       def test_add_goods(self):
           get_token()
           add_to_shopping_trolley()
   
       @allure.story("商品加入购物车")
       @allure.title("异常用例--将库存数=0的商品加入购物车")
       @allure.description("校验库存数为0的商品加入购物车是否提示正确的错误信息")
       @allure.severity("normal")
       def test_add_goods_error(self):
           get_token()
           add_to_shopping_trolley()
   
       @allure.story("查询购物车商品数量")
       @allure.title("查询购物车所有商品的总数量")
       @allure.description("校验查询购物车所有商品的总数量是否正常")
       @allure.severity("critical")
       def test_get_goods_quantity(self):
           get_token()
           add_to_shopping_trolley()
           get_shopping_trolley_goods()
   
       @allure.story("查询购物车商品数量")
       @allure.title("查询购物车单个商品的数量")
       @allure.description("校验查询购物车单个商品的数量是否正常")
       @allure.severity("critical")
       def test_get_goods_quantity(self):
           get_token()
           add_to_shopping_trolley()
           get_shopping_trolley_goods()
   
       @allure.story("清空购物车")
       @allure.title("加入商品后再清空购物车")
       @allure.description("校验清空购物车接口功能是否正常")
       @allure.severity("normal")
       def test_empty_shopping_trolley(self):
           get_token()
           add_to_shopping_trolley()
           empty_shopping_trolley()
   
   
   @allure.epic("xx在线购物平台接口测试")
   @allure.feature("下单模块")
   class TestPlaceOrder:
   
       @allure.story("购物车下单")
       @allure.title("商品加入购物车再下单")
       @allure.description("校验清购物车下单功能是否正常")
       @allure.severity("critical")
       def test_place_order(self):
           get_token()
           add_to_shopping_trolley()
           place_order()
   
       @allure.story("立即购买下单")
       @allure.title("选择商品不加入购物车立即购买下单")
       @allure.description("校验立即购买下单功能是否正常")
       @allure.severity("critical")
       def test_order(self):
           get_token()
           place_order()
   ```

4. 下面对常用的allure方法做一个说明

   - `@allure.epic()`，用于描述被测软件系统

   - `@allure.feature()`，用于描述被测软件的某个功能模块

   - `@allure.story()`，用于描述功能模块下的功能点或功能场景，也即测试需求

   - `@allure.title()`，用于定义测试用例标题

   - `@allure.description()`，用于测试用例的说明描述

   - `@allure.link()` ，用于测试用例添加链接，传入链接和名称

   - `@allure.issue()` ，用于测试用例添加缺陷，传入缺陷链接和名称，link的封装

   - `@allure.testcase()` ，用于测试用例添加关联的功能用例，传入功能用例链接和名称，link的封装

   - `@allure.severity()`，标记测试用例级别，由高到低分为 blocker、critical、normal、minor、trivial 五级，实际工程代码建议使用allure提供的枚举类，Dynamic 类不支持。

     ```python
     class Severity(str, Enum):
         BLOCKER = 'blocker'
         CRITICAL = 'critical'
         NORMAL = 'normal'
         MINOR = 'minor'
         TRIVIAL = 'trivial'
         
     # 像这样使用
     @allure.severity(Severity.BLOCKER)
     ```

   - `@allure.step()`，标记通用函数使之成为测试步骤，测试方法/测试函数中调用此通用函数的地方会向报告中输出步骤描述，Dynamic 类不支持。

   - `@allure.attach()` ，用于测试用例添加附件，主要是针对stream类型的数据，会保存为指定的文件出现在报告中

   - `@allure.attach.file() `，用于测试用例添加附件，主要是针对已有文件，展示到报告中

5. 执行测试

   ```python
   pytest --alluredir temp_dir [options]
   
   # allure 相关参数说明
   #       --alluredir=temp_dir		指定测试结果的目录路径，此时的文件还不是报告，是allure收集的一些统计数据
   #       --clean-alluredir		如果已经存在报告，就先清空它
   #       --allure-no-capture		不加载 logging/stdout/stderr 文件到报告
   #				--allure-epics=epic名称		选择运行某些epic标记的用例
   #       --allure-features=模块名称		选择运行某些feature标记的用例
   #       --allure-stories=子模块名称		选择运行某些story标记的用例
   ```

6. 生成报告。这时候就需要使用Allure的命令行工具

   ```shell
   # temp_dir 上一步存放中间结果数据的目录
   # report_dir 存放报告的目录，不能和temp_dir是一个目录
   allure generate temp_dir -o report_dir --clean
   ```

7. 其他Allure命令

   ```shell
   # 生成报告，并启动一个服务以供外界访问
   allure serve temp_dir
   
   # 使用已经生成的报告启动服务
   allure open report_dir
   
   
   # 上面两个命令都可以使用选项参数指定 ip和port
   #   -h,-host  host
   #   -p,-port  port
   ```

   



















