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

   



