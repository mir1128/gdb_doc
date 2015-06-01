# 大规模存量代码DT实践之路

@(Temp)

# 背景

# 实践

## 解决耦合过多，设计不足的实践

### 框架代码与业务代码过度耦合

每个大型项目都有一些框架代码，与之相对的是业务代码。在开发的过程中必须小心对这二者进行甄别并用“中间层”将它们隔离。框架代码(不包括`Utils`这样“无害”的工具类)大量侵入业务代码带来的是理解困难和不可测试。理解困难是因为阅读代码时必须在框架和业务之间切换，对于新接触代码的人来说很难分清它们的区别，而框架代码由于抽象层次较高，难以获得感性认识；不可测试则是因为框架代码通常是一个较长调用链，必须对上下游类进行mock才能让测试运行起来。如果能在系统构建之初提供了这样一套mock类还好，否则很难期望后续的维护开发人员有能力构造出来。

下面是M2000一个典型进程的结构

`img src="process.png"`

一个进程中包含了若干模块，这些模块由一个框架类`Kernel`进行集中管理。
``` cpp
//kernel.hpp
class Kernel
{
public:
   	virtual KernelModule & kernelModule(::std::string const & moduleName) = 0;
   	virtual KernelModule * findKernelModule(::std::string const & moduleName) = 0;
};

template<typename T>
T& kernelModule(Kernel& kernel) {
   	return dynamic_cast<T&>(kernel.kernelModule(T::_moduleName()));
}

//kernelModule.hpp
class KernelModule
{
public:
   	virtual Kernel& kernel(void) = 0;
};

//某功能模块
class SomeModule : public KernelModule
{
public:
   	static const std::string _moduleName(void);
	virtual void doSomeThing();
};
```

`SomeModule::doSomeThing()`是某个完成业务功能的函数。在实现业务逻辑的时, 对其他模块的依赖是不可避免的. 例如在`SomeModule::doSomeThing()`中需要访问属于`ModuleA`的服务`ServiceClass`时，写出来的代码是这样的：

``` cpp
void SomeModule::doSomeThing()
{
   	ModuleA& moduleA = kernelModule<ModuleA>(kernel());
    ServiceClass& someService = moduleA.getService();
   	// do something with someService
}
```

为了访问`ServiceClass`, 这段代码做了两件事情, 首先是通过框架提供的`Kernel`类拿到了`ModuleA`的引用, 接着从`ModuleA`中获取`ServiceClass`的实例进行调用.

这段代码并不难理解, 逻辑清晰直接. 但当我们想针对`SomeModule::doSomeThing()`进行单元测试时, 我们需要在测试代码中构造出`ServiceCalss`, `ModuleA`以及框架相关的`Kernel`等一系列依赖. 同时这些依赖和其他模块可能还有千丝万缕的关系, 将他们全部构造出来往往很不现实. 退一步讲, 即使我们能够构造出所有依赖进行测试, 这个用例也会十分脆弱, 任何一个依赖的行为变化都可能导致这个用例执行失败.

为了顺利的对`SomeModule::doSomeThing()`进行单元测试, 我们需要首先解决以下两点问题:
* 如何构造出所依赖的`ServiceClass`并确保它表现出我们期望的行为
* 如何保证执行测试时, 通过框架的`Kernel`类返回我们期望的`ModuleA`进而返回我们期望的`ServiceClass`实例

对于第一点, 我们可以对`ServiceClass`抽象出接口, 并且针对这个接口实现一个Mock, 之后便可以通过这个Mock的`ServiceClass`来设置我们想要的期望. (关于Mock的介绍可以参考[这里](http://www.ibm.com/developerworks/cn/linux/l-cn-cppunittest/#3.%E5%BA%94%E7%94%A8%20googlemock%20%E7%BC%96%E5%86%99%20Mock%20Objects%7Coutline))

实现了`ServiceClass`的Mock后, 我们解决了这个依赖的构造和行为控制问题. 这时我们可以开始思考如何处理第二个问题: 如何让框架类`Kernel`和`ModuleA`返回我们创造的Mock对象.

我们再次审视一下`SomeModule::doSomeThing()`的逻辑, 在这段代码中, 我们真正想做的事情是通过`ServiceClass`完成一些功能, 无论`Kernel`或是`ModuleA`只是用来帮助我们获取`ServiceClass`的实例. 换种说法就是`SomeModule::doSomeThing()`依赖于`ServiceClass`而不是`Kernel`和`ModuleA`.

明确了`SomeModule::doSomeThing()`, 我们就可以着手进行一些重构, 让`SomeModule`以最小的依赖来`doSomeThing()`:

首先我们将`SomeModule::doSomeThing()`抽取出接口, 明确SomeModule的职责:
``` cpp
// SomeModuleInterface.hpp
class SomeModuleInterface
{
public:
   	virtual void doSomeThing() = 0;
};
```

接下来我们来实现`SomeModuleInterface`:
``` cpp
// SomeModule.cpp
class SomeModule : public SomeModuleInterface
{
public:
   	SomeModuleImpl(ServiceClass& someService) 
   	 : someService_(someService) {
   	}
    virtual void doSomeThing() {
	    // do something with someService_
    }
private:
   	ServiceClass& someService_;
};
```

通过将依赖的`ServiceClass`注入,  `SomeModule`摆脱了对`Kernel`的依赖, 通过构造函数将最小依赖传入.

这时`SomeModule`已经完成它所要实现的功能, 并且能够通过传入Mock的`ServiceClass`来完成单元测试, 下一步要做的事情就是将`SomeModule`与框架结合起来, 使其能够在生产环境被加载和运行起来:

``` cpp
//SomeModuleImpl.hpp
class SomeModuleImpl: public SomeModule,
                      public KernelModule
{
public:
	SomeModuleImpl() 
	  : SomeModule(kernelModule<ModuleA>(kernel()).getService()) {
	}

   	static const std::string _moduleName(void);
};
```
`SomeModuleImpl`通过继承`KernelModule`来获得框架提供的能力, 例如通过`Kernel`获取`ModuleA`及`SomeService`的实例. 同时它又通过继承`SomeModule`来实现`SomeModuleInterface`, 提供`doSomeThing()`的逻辑, 并且用从框架类中获取到的`SomeService`来构造`SomeModule`.

这样`SomeModuleInterface`及`SomeModule`负责业务实现, 可以十分方便的通过Mock和依赖注入实现单元测试, 而`SomeModuleImpl`则是负责隔离框架和业务的"中间层", 负责对业务类进行构造和初始化.

### 与数据库、网络相关的测试方案

单元测试如果依赖于网络和数据库不但让测试环境构造变得困难，而且不稳定。依赖注入是解决模块依赖的有效手段，将网络收发信息操作和数据访问操作抽象成接口注入的到业务类中就可以消除对数据库和网络的依赖。

不使用依赖注入的实现：

``` cpp
class SomeClass
{
public:
    void doSomeThing()
    {
        std::string sql = "select * from sometable";
        DbConnection& connection = DbConnectionManager::getInstance().getconnection();
        DbRecord record = connection.Execute(sql);
        ... ...
    }
};
```
把对数据库的链接当做参数就变成：

``` cpp
class DbConnectionInterface
{
public:
    virtual DbRecord Execute(std::string) = 0;
};

class SomeClass
{
public:
    void doSomeThing(DbConnectionInterface& connection = DbConnectionManager::getInstance().getconnection())
    {
        std::string sql = "select * from sometable";
        DbRecord record = connection.Execute(sql);
    }
};
```

### 与线程相关的测试方案

对于线程的单元测试应该分为两步来进行：1. 验证线程启动参数是否符合预期。 2.验证线程函数功能是否正常

一个典型的线程封装类：
``` cpp
//somethread.h
class SomeThread
{
public:
	static void run(void* parameter)
	{
		SomeThread* threadContext = (SomeThread*)parameter;
		SomeData& data = threadContext->getSomeData();
		//do something with data;
	}

	SomeData& getSomeData()
	{
		return someData_;
	}

private:
	SomeData someData_;
};

//someservice.h
class SomeService
{
public:
	SomeService(std::vector<std::shared_ptr<SomeData> > datas):datas_(datas){}

	void startService(){
	for (auto data : datas_)
	{
		_beginthread(SomeThread::run, 0, data.get())
	}
}

private:
	std::vector<std::shared_ptr<SomeData> > datas_;
};
```

对于线程启动代码(SomeService.startService)验证它的启动参数是否正确。

EXPECT_CALL(mockThreadStarter, startService(SomeMatchers(xxx))).WillRepeatedly(Return(0));

对于线程函数验证：

``` cpp
TEST(SomeThreadSpec, ShouldRunNormally)
{
	SomeThread threadContext;
	//some expectation;
	SomeThread::run((void*)&threadContext);
}
```

### 与时间相关的测试方案

假如某个类在每天凌晨3点删除前一天的日志文件:

``` cpp
class Schedluer
{
public:
   	void run()
    {
       	Time checkTime;
        checkTime.setHour(3); //每天3点

   	    TimeSpan interval;
       	interval.setMiniute(1); //run每分检查一次

        if (abs(getCurrentTime() - checkTime) < interval)
   	    {
       	    deleteFiles(...);
        }
   	}
}
```

如果想测试Schedluer删除日志文件的功能，最直接的办法就是修改系统时间。

但是如果对代码稍作变化就会有不一样的效果：

``` cpp
class Schedluer
{
public:
   	Schedluer（TimerInerface* timerInface）
    void run()
   	{
       	TimeSpan interval;
        interval.setMiniute(1); //run每分钟跑一次

   	    if (abs(getCurrentTime() - checkTime) < timerInface_->getCheckTime())
       	{
           	deleteFiles(...);
        }
   	}
private:
   	TimerInerface* timerInface_;
}
```
引入了一个TimerInerface接口类

``` cpp
class TimerInerface
{
public:
    virtual Time getCheckTime() = 0;
    ...
    virtual ~TimerInerface(){};
}
```

模块中与时间相关的宏，变量都改为调用TimerInerface的某个成员函数。然后修改测试用例：

``` cpp
class MockTimerInerface : public TimerInerface
{
public:
    MOCK_METHOD(getCheckTime, Time());
}

TEST(SchedluerTestSuit, ShouldDeteteLogFileAt3OclockEveryDay)
{
    MockTimerInerface mock;

    Time tm;
    tm.setHour(3);

    EXPECT_CALL(mock, getCheckTime()).WillRepeatly(Return(tm));

    Schedluer scheduler(&mock);
    scheduler.run();

    ASSERT_TURE(...) ; //检查文件是否存在
}
```

## 解决mock库支持不足的实践

gmock是一款优秀的mock工具，它是基于c++语法规则的，使用继承，多态实现对真实对象的替换。但是在存量代码中可能存在一些依赖较多的类，如果将这些依赖全部通过注入的方式会对现有代码进行大量的修改，在测试不足的条件下可能会引入更多风险，因此需要一款二进制级的mock库，通过修改函数地址的方式实现对依赖的替换。能满足这个需求的有AMock(华为自研)、FakeIt(只支持c++11)、Mockcpp，microsoft的detours可以完成函数地址替换，但是不提供验证功能。它们的基本原理是：

`img src="/Users/jieliu/Downloads/mock.png" width="600"`

被替换的函数(target function)前5个字节被替换为一条jmp指令，被调用时就会跳转到我们实现的mock函数。由于mock函数的签名与被测函数完全一致，因此这种替换对于产品来说完全是透明的。

自由函数和类成员函数地址替换略有不同(成员函数第一个参数是this指针)，但实现原理是一样的。关于函数地址替换的更多原理请参考：http://research.microsoft.com/en-us/projects/detours/


依赖注入和二进制替换各有利弊：依赖注入可以有效改善代码结构，方便测试，但同时也意味着更多的修改。对于一个已经处于稳定期，只进行增量开发的产品来说有时这种修改不利于产品的稳定；二进制替换的方式不需要修改产品代码，但不能驱动出更好的代码结构，如果滥用会让测试失去应有的意义。测试除了验证产品功能的正确性，还应该是一份很好的产品说明书，新人可以通过阅读测试了解模块的功能。

在实际项目中我们采用了以gmock为主，同时结合mockcpp的方式进行mock. 用依赖注入的方式对整体框架设计进行解耦，对于个别函数用mockcpp进行mock.


## 解决人员测试技能不足的实践

### workshop

为了让DT顺利开展，我们针对开发人员进行了以下培训：

* gtest/gmock/mockcpp使用
* 如何用依赖注入的方式解耦
* 如何Mock一些复杂场景

workshop以练习为主，每次课围绕着一个精心设计的例子进行，通过两个小时的练习掌握一个知识点，经过4-5次培训开发人员对如何写测试有了基本的了解。

### 结对

在workshop中学到的内容偏理论，如果想把理论用在产品中还需要解决一些诸如编译失败、程序崩溃等具体问题，结对就是同开发人员一起针对产品中的某个具体类完成单元测试。通过结对帮助开发人员消除开始写测试的不适。

### 独立完成部分模块测试

在该项目中我们还独立承担了部分模块的开发，该部分代码都有精心设计的用例保证功能正确性,并且作为参考范例。

#其他

一 增加测试是否需要修改现有代码？

对现有的代码进行重构可以改善阅读体验，增加可维护性，但同时也带来了风险，有可能会影响到现有特性，因此需要对修改风险和收益做权衡。对于一些已经稳定的很少做修改的代码尽量不修改或者少修改，对于经常做增量开发的代码可以边重构边写测试。

二 如何加强开发人员写测试的意愿？

粗放式的开发方式（不写测试）是通过在联调阶段发现问题的，风险集中在联调阶段。使用测试驱动的方式可以将风险分摊在开发过程中，但是对于没有这种经历的开发人员来说很难体会到这样做的好处。因此在项目启动之初需要依赖一些管理手段来达到效果，当开发人员体会到测试带来的好处以后，会主动推动完成测试。


#总结

测试是将手动验证的过程用代码固化下来，这种固化省去了后面局部修改再验证的工作量，同时它还是一份最好的产品说明书，对于其他人了解代码有很大的帮助，但是对于从事存量代码开发的人来说，写测试的意愿普遍不高。这就需要项目管理者对测试意义有足够的理解，并且有决心坚持完成并见到最终成果.
