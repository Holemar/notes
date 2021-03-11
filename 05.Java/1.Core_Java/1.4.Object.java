﻿
对象(物件)

名词
    对象:
    类:   一类属性相同的对象
    属性: 是什么样
    方法: 能做什么(C 中叫作函数)

    成员: 包括变量和方法
    成员变量: 包括实例变量和静态变量


对象:
    声明: Student s ;
        这时我们只是说明s是一个能够指向Student类型的引用(相当于C++中的指针),并没有创建一个对象。
        所以我们此时不能对s做任何操作。
    初始化: s = new Student();
        向系统申请一块存储空间(地址空间)，该地址空间保存的是一个Student类型的数据。
        而s中保存的就是该地址空间的首地址。
    变量: 内存空间中一块具有固定长度的，用来保存数据的地址空间。(s也是一个变量)
    一个对象可以有多个引用指向。
      Student[] s = new Student[3]  只是相当于声明一个长度为 3 的Student类型的数组。


在java中对面向对象(OO)的要求
    1．对象是客观存在的，万物皆对象。
        (注: 看不见的对象并不表示该对象不存在，比如说事件)；
    2．简单性: 采用面向对象方法可以使系统各部分各司其职各尽所能。
    3．复用性: 对象的功能越简单其可重用性越高。
    4．弱耦合性: 各司其职各尽所能。
    5．高内聚性: 一个对象独立完成一个功能的能力
    6．类是一类事务的共性，是人类主观认识的一种抽象，是对象的模板。


面向过程与面向对象的对比
    面向过程: 先有算法，后有数据结构。先考虑怎么做。
    面向对象: 先有数据结构，后有算法。先考虑用什么做。


创建对象的步骤
    1、分配空间
    2、初始化属性
    3、调用构造方法
    注: 构造方法不能手工调用，在对象的生命周期内构造方法只调用一次。


构造方法
    构造方法是在生成对象的过程中调用的方法，但构造方法并不能创建对象。
        new 对象的时候需要调用构造方法。
    1、特点: 没有返回值(连void也没有)，方法名与类名相同。(如果加上 void 会变成普通方法。)
    2、在不写构造方法时，系统会自动生成一个无参的构造方法。
    3、请养成在每个类中自己加上无参构造方法的习惯。

    格式为: public ClassName(){}
        构造方法也可以是其它的限制符―― private protected default
        private 一般用在 singleton 模式中。
    在一个对象的生成周期中构造方法只用一次，一旦这个对象生成，那么这个构造方法失效。
    * 接口不能创建实例，因为没有构造方法

    可以构造多个构造方法，但多个构造方法的参数表一定不同，或参数顺序不同
    即属于不同的构造方法: -----------------------> 构造方法的重载

    使用构造方法来初始化对象的状态: 把初始化代码放到构造方法中，并且把构造方法设定成需要参数的
    编译器一定会帮你写出没有参数的构造方法吗？不会
        如果你已经写了一个有参数的构造方法，并且你需要一个没有参数的构造方法，则你必须自己动手写
        如果类有一个以上的构造方法,则参数列表一定要不一样，我们可以认为这几个构造方法形成重载关系
        如果我们提供了有参的构造方法，那么系统不会再提供无参的构造方法了。
        这样当被子类继承时，如果子类构造方法不人为调用父类的有参构造方法就会出现异常。
    构造方法可以通过 this 调用另外一个构造方法(this 此时必须在第一行语句)


匿名对象:
    创建对象时，直接调用对象的方法而不定义对象的句柄。
        如:  person p1 = new person; p1.shout();
        改写成:  new person.shout();   //此方法执行完，此匿名对象也就变成了垃圾。
    使用匿名对象的情况:
        1. 此对象只需要一次方法调用。
        2. 此对象作为实参传给一个函数调用。


this 当前对象
    谁调用该方法，在这一时刻谁就是该方法的当前对象；是个隐式参数，代表被构造的对象。
    用 this 来区分实例变量和局部变量。
      this.实例变量名 ＝ 局部变量名    (将局部变量赋值给实例变量)
   this()表示调用本类的其它构造方法，且只能放在一个方法中的第一行第一句。
        构造方法可以通过this调用另外一个构造方法(this此时必须在第一行语句)
*super 关键字也是个隐形参数，代表被构造对象的父类。
    同样也必须在构造方法的第一行


对象和对象引用的区别
   对象好比一台电视机，对象引用好比电视机遥控。对象引用 中存的是对象的地址。
   多个对象引用中存放的是同一个地址，表示该对象被多个对象引用所引用。


面向对象的三大特性:
    封装(Encapsulation)、继承(Inheritance)、多态(polymiorphism)


封装:
    1．定义: 指一个对象的内部状态对外界是透明的，对象与对象之间只关心对方有什么方法，而不关心属性。
       封装使实现的改变对架构的影响最小化。封装后的代码更具有安全性、可扩展性和可维护性。
    2．原则: 封装使对象的属性尽可能的私有，根据需要配上相应的get/set方法，对象的方法尽可能的公开。
           该隐藏的一定要隐藏，该公开的一定要公开。
    3．方法公开的是声明而不是实现。使方法实现的改变对架构的影响最小化。
    4．访问权限控制从严到宽
       private  :仅本类成员可见
       default  :本类＋同包类可见(默认)
       protected:本类＋同包＋不同包的子类
       public   :公开
        注: 这里的同包指的是跟父类所在的包相同。
    5、完全封装: 属性全部私有，并提供相应的get/set方法。
    优点:
    1．事物的内部实现细节隐藏起来
    2．对外提供一致的公共的接口――间接访问隐藏数据
    3．可维护性


一、继承:
    1 定义: 基于一个已存在的类构造一个新类。
      继承已存在的类就是复用这些类的方法和属性，在此基础上，还可以在新类中添加一些新的方法和属性。
    2 父类到子类是从一般到特殊的关系。
    3 继承用关键字 extends
      dog extends Animal :表示狗类继承了动物类
    4 Java中只允许单继承(java简单性的体现)
      父子类之间的关系是树状关系。(而多继承是网状关系)
    5 父类中的私有属性可以继承但是不能访问。
      也可以说父类中的私有属性子类不能继承。
    6 原则: 父类放共性，子类放个性。
    7 构造方法不能被子类继承。

    父类的成员能否继承到子类？
      private: 本类内部可以访问  不能继承到子类
     (default): 本类内部可以访问，同包其它类也可以访问
            能否继承到子类？ 不一定: 同包的可继承，不同包则不可继承。
      protected: 本类内部可以访问，不同包的子类也可以访问， 同包其它类也可以访问
            能继承到子类
      public: 任何地方都可以访问  能继承到子类

    继承的意义:
    1. 避免了重复的程序代码，提高了程序的可重用性
    2. 定义出共同的协议


二、带继承关系的对象创建的过程
    1．递归的构造父类对象
    2．分配空间
    3．初始化属性
    4．调用本类的构造方法

三、 super 关键字
    1. super()表示调用父类的构造方法
    2. super()也和 this 一样必须放在构造方法的第一行第一句。不是构造方法则不用第一行。
    3. super.表示调用父类的方法或属性。例: super.m();
    4. super 可以屏蔽子类属性和父类属性重名时带来的冲突
    5．在子类的构造函数中如果没有指定调用父类的哪一个构造方法，就会调用父类的无参构造方法，即super()

    指向父类的引用
     super.age
     super.addAge()
    调用父类的构造方法
     super();
     super("wangcai",8);


一个对象的创建过程
    1. 当构造一个对象的时候，系统先构造父类对象，再构造子类对象。
    2. 构造一个对象的顺序: (注意: 构造父类对象的时候也是这几步)
       递归地创建父类的 static 成员(即使只调用其子类静态成员，也会先创建父类静态成员)；
       顺序地创建本类的 static 成员(只要调用这个类的属性或方法都需创建一次)；
       递归地创建父类对象(先创建父类非静态成员，再调用父类构造方法)；
       顺序地创建本类非静态成员(包括属性和方法)；
       调用本类的构造方法(它可调用本类或父类的成员，也可调用本类的其它构造方法)。
       创建完成了(更多详情参看下面: 类加载的顺序)


四、白箱复用和黑箱复用
    1．白箱复用: 又叫继承复用，子类会继承父类所有的东西，
        从某种程度上说白箱复用破坏了封装。是一种 is a 的关系。
    例: class Liucy{
          public void teachCpp(){System.out.println("Teach Cpp");}
          public void chimogu(){ }
        }
       class Huxy extends Liucy{}

    2、黑箱复用: 又叫组合复用，是一种 has a 的关系。
    例: class Liucy{
          public void teachCpp(){System.out.println("Teach Cpp");}
          public void chimogu(){    }
        }
       class Huxy {
          private Liucy liucy = new Liucy();
          public void teachCpp(){liucy.teachCpp();}
        }
    原则: 组合复用取代继承复用原则。
         使我们可以有机会选择该复用的功能。


多态
    1．定义: 是指一个对象可以有多种形态，换句话说多态使我们可以把一个子类对象看作是一个父类对象类型
       (例: father A = new child() )。
       多态指的是编译时的类型变化，而运行时类型不变。
    2．多态分为两种: 编译时多态和运行时多态。
       编译时类型: 定义时类型(主观概念)把它看作什么。
       运行时类型: 真实类型(客观概念) 实际上他是什么。
       重载是编译时多态，覆盖是运行时多态。在方法重载的情况下，参数类型决定于编译时类型。
    3．作用: 在需要一类对象的共性时，可以很容易的抽取。并且可以屏蔽不同子类对象之间所不关心的差异。
       多态方便写出更通用的代码，以适应需求的不断变化
    4．多态常见的用法:
       (1)、多态用在方法的参数上
       (2)、多态用在方法的返回类型上
    5．运行时多态的三原则:
       (1)、对象不变(改变的是主观认识)
       (2)、对于对象的调用只能限于编译时类型的方法。
       (3)、在程序的运行时，动态类型判定。运行时调用运行时类型，即他调用覆盖后的方法。
    注意: 多态时，只有一般方法是动态调用的；而 static 方法和 final 方法依然是静态调用的；属性全是静态调用的。
     如: father A = new child(); 则A的一般方法是child的方法；但A的属性是father的属性。
    同样: child C = new child(); 则 (father)C 的一般方法还是child的方法，但属性是father的属性。

    if(cat instanceof Animal){ ... }  //如果cat属于Animal类型则执行
    强制类型转换，在迫不得已的时候再用。因为很容易出错。


什么时候类加载
    第一次需要使用类信息时加载。
    类加载的原则: 延迟加载，能不加载就不加载。

触发类加载的几种情况:
    (1)、调用静态成员时，会加载静态成员真正所在的类及其父类。
         通过子类调用父类的静态成员时，只会加载父类而不会加载子类。
    (2)、第一次 new 对象的时候 加载(第二次再 new 同一个类时，不需再加载)。
    (3)、加载子类会先加载父类。
        注: 如果静态属性有 final 修饰时，则不会加载，当成常量使用。
           例: public static final int a =123;
        但是如果上面的等式右值改成表达式(且该表达式在编译时不能确定其值)时则会加载类。
           例: public static final int a = math.PI
        如果访问的是类的公开静态常量，那么如果编译器在编译的时候能确定这个常量的值，就不会被加载；
        如果编译时不能确定其值的话，则运行时加载


类加载的顺序:
    1.加载静态成员/代码块:
      先递归地加载父类的静态成员/代码块(Object的最先)；再依次加载到本类的静态成员。
      同一个类里的静态成员/代码块，按写代码的顺序加载。
      如果其间调用静态方法，则调用时会先运行静态方法，再继续加载。同一个类里调用静态方法时，可以不理会写代码的顺序。
      调用父类的静态成员，可以像调用自己的一样；但调用其子类的静态成员，必须使用“子类名.成员名”来调用。
    2.加载非静态成员/代码块:
      先递归地加载父类的非静态成员/代码块(Object的最先)；再依次加载到本类的非静态成员。
      同一个类里的非静态成员/代码块，按写代码的顺序加载。同一个类里调用方法时，可以不理会写代码的顺序。
      但调用属性时，必须注意加载顺序。一般编译不通过，如果能在加载前调用，值为默认初始值(如: null 或者 0)。
      调用父类的非静态成员(private 除外)，也可以像调用自己的一样。
    3.调用构造方法:
      先递归地调用父类的构造方法(Object的最先)；默认调用父类空参的，也可在第一行写明调用父类某个带参的。
      再依次到本类的构造方法；构造方法内，也可在第一行写明调用某个本类其它的构造方法。
    注意: 如果加载时遇到 override 的成员，可看作是所需创建的类型赋值给当前类型。
      其调用按多态用法: 只有非静态方法有多态；而静态方法、静态属性、非静态属性都没有多态。
      假设子类override父类的所有成员，包括静态成员、非静态属性和非静态方法。
      由于构造子类时会先构造父类；而构造父类时，其所用的静态成员和非静态属性是父类的，但非静态方法却是子类的；
      由于构造父类时，子类并未加载；如果此时所调用的非静态方法里有成员，则这个成员是子类的，且非静态属性是默认初始值的。




final 修饰符
    (最终的、最后的)当 final 修饰时，不能被改变，不能被继承
    1. final 可以用来修饰类、属性和方法、局部变量。
    2. final 修饰一个属性时，该属性成为常量。
     (1)对于在构造方法中利用final进行赋值时，此时在构造之前系统设置的默认值相对于构造方法失效。
     (2)对于实例常量的赋值有两次机会
         在初始化的时候通过声明赋值
         在构造的时候(构造方法里)赋值
         注: 不能在声明时赋值一次，在构造时再赋值一次。
         注意: 当 final 修饰实例变量时，实例变量不会自动初始化为0；但必须给他赋值才能通过编译。
    3. final 修饰方法时，该方法成为一个不可覆盖的方法。这样可以保持方法的稳定性。
       如果一个方法前有修饰词 private 或 static, 则系统会自动在前面加上 final 。
       即 private 和 static 方法默认均为 final 方法。
    4. final 常常和 static, public 配合来修饰一个实例变量，表示为一个全类公有的公开静态常量。
       例:  public static final int a = 33;
       在这种情况下属性虽然公开了，但由于是一个静态常量所以并不算破坏类的封装。
    5. final 修饰类时，此类不可被继承，即 final 类没有子类。
       一个 final 类中的所有方法默认全是 final 方法。
       final 不能修饰构造方法，构造方法不能被继承更谈不上被子类方法覆盖。

关于 final 的设计模式: 不变模式
    1、不变模式: 一个对象一旦产生就不可能再修改(String 就是典型的不变模式)；
         通过不变模式可以做到对象共享；
    2、池化思想: 用一个存储区域来存放一些公用资源以减少存储空间的开销。
         有池的类型:boolean,byte,int,short,long,char,(池范围在-127~128之间)
         (float,double 等小数没有池)
         例: 在String类中有个串池(在代码区)。
         池: 堆里的一片独立空间。目的是拿空间换时间，让运算效率更高。
     (1)如果用Stirng str = "abc" 来创建一个对象时，则系统会先在“串池”中寻找有没有“abc”这个字符串
         如果有则直接将对象指向串池中对应的地址，如果没有则在串池中创建一个“abc”字符串。
         所以: String str1 = "abc";
         String str2 = "abc";
         Str1 == str2 返回值是ture;他们的地址是一样的。
           也就是说str1和str2都指向了代码空间中相同的一个地址，而这个地址空间保存就是是字符串"abc"
         字符串是不可改变的类型，所以可以共享。所以串池里不会有相同的两个字符串。

     (2)如果用 String str = new String("abc")则直接开辟一块内存放"abc"这个字符串。
         所以上面这语句，创建两个"abc"，一个在池，一个是对象
         String str2 = new String("abc");
         Str == str2 返回值是false;他们的地址是不一样的。
         即是说str和str2分别指向了堆空间中不同的两个地址，而这两个地址空间保存的都是字符串"abc"

abstract 抽象
    1. 可用来修饰类、方法
    2. abstract 修饰类时，则该类成为一个抽象类。
       抽象类不可生成对象(但可以有构造方法留给子类使用),必须被继承使用。
       抽象类可以声明，作为编译时类型，但不能作为运行时类型。
       abstract 永远不会和 private,static,final 同时出现。( 因为抽象必须被继承。)
    3. abstract 修饰方法时，则该方法成为一个抽象方法，抽象方法不能有实现；由子类覆盖后实现。
       比较: private void print(){};表示方法的空实现
       abstract void print();表示方法为抽象方法，没有实现
    4. 抽象方法从某中意义上来说是制定了一个标准，父类并不实现，留给子类去实现。
       注: 抽象类中不一定要有抽象方法，但有抽象方法的类一定是抽象类。
       抽象类可以有抽象方法和非抽象方法。实现抽象类的第一个具体类必须实现其所有抽象方法。
    5. 关于抽象类的设计模式: 模板方法
        灵活性和不变性

interface 接口
    1、定义: 接口不是类，而是一组对类需求的描述，这些类要遵从接口描述的统一格式进行定义。
       定义一个接口用关键字 interface 。
       例: public interface a{……}
    2、接口是一种特殊的抽象类。
       在一个接口中，所有的方法为公开、抽象的方法，所有的属性都是公开、静态、常量。
       所以接口中的所有属性可省略修饰符: public static final。也只能用这三个修饰符。
       接口中所有的方法可省略修饰符: public abstract。但这些都是默认存在的。
    3、一个类实现一个接口必须实现接口中所有的方法，否则其为一抽象类。而且实现类的方法需要 public
       实现接口用关键字 implements.
       所谓实现一个接口就是实现接口中所有的方法。
       例: class Aimple implements A{……..};
    4、一个类除了继承另一个类外(且只能继承一个类),还可以实现多个接口(接口之间用逗号分割)。
       接口可以实现变相的多继承。
       例: class Aimple extends Arrylist implements A,B,C{…}
    5、不能用“new 接口名”来实例化一个接口，但可以声明一个接口。
    6、接口与接口之间可以多继承。
       例: interface face1 extends face2,face3{}
       接口的继承相当于接口的合并
    7、接口的作用
     (1)、间接实现多继承。
           用接口来实现多继承并不会增加类关系的复杂度。因为接口不是类,是在类的基础上的再次抽象。
           父类: 主类型     接口: 副类型
           典例: 父亲(主)  和  老师(副)
     (2)、允许我们为一个类定义出混合类型。
     (3)、通过接口制定标准
            接      口: 标准的定义  定义标准
            接口的调用者: 标准的使用  使用标准
            接口的实现类: 标准的实现  实现标准
        接口的回调:先有接口的使用者，再有接口的实现者，最后把接口的实现者的对象传到接口的使用者中，
                 并由接口的使用者通过接口来调用接口实现者的方法。
        例: sun公司提供一套访问数据库的接口(标准)，java程序员访问数据库时针对数据库接口编程。
           接口由各个数据库厂商负责实现。
     (4)、解耦合作用: 采用接口可以最大限度的做到弱耦合，将标准的实现者与标准的制定者隔离
         (例: 我们通过JDBC接口来屏蔽底层数据库的差异)
    8、接口的编程设计原则
     (1)、尽量针对接口编程(能用接口就尽量用接口)
     (2)、接口隔离原则(用若干个小接口取代一个大接口)
           这样可以只暴露想暴露的方法，实现一个更高层次的封装。
    9、注意点:
     (1)、一个文件只能有一个 public 接口，且与文件名相同。
     (2)、在一个文件中不能同时定义一个 public 接口和一个 public 类。
     (3)、接口与实体类之间只有实现关系，没有继承关系；
          抽象类与类之间只有继承关系没有实现关系。接口与接口之间只有继承关系，且允许多继承。
     (4)、接口中可以不写 public,但在子类实现接口的过程中 public 不可省略。

接口 VS 抽象类
    1、接口中不能有具体的实现，但抽象类可以。
    2、一个类要实现一个接口必须实现其里面所有的方法，而抽象类不必。
    3、通过接口可以实现多继承，而抽象类做不到。
    4、接口不能有构造方法，而抽象类可以。
    5、实体类与接口之间只有实现关系，而实体类与抽象类只有继承关系
      抽象类与接口之间既有实现关系又有继承关系。
    6、接口中的方法默认都是公开抽象方法，属性默认都是公开静态常量，而抽象类不是。


修饰符的使用情况:
(Y表可用；不写表示不可用)
    修饰符         类       属性        方法      局部变量(所有局部变量都不能用修饰符)
    public        Y         Y          Y
    protected               Y          Y
    (default)     Y         Y          Y
    private                 Y          Y
    static                  Y          Y
    final         Y         Y          Y         Y
    abstract      Y                    Y

访问权限控制:
    修饰符      同一个类    同一个包  (不同包)子类  其它包
    public        Y         Y          Y       Y
    protected     Y         Y          Y
    (default)     Y         Y
    private       Y



Object 类
   1、 Object 类是类层次结构的根类，他是所有类默认的父类。
   2、 Object 类中的其中三个方法。
    (1)、finalize()
        当一个对象被垃圾收集的时候，最后会由JVM调用这个对象的finalize方法；
        注意: 这个方法一般不用，也不能将释放资源的代码放在这个方法里；只有调用C程序时，才可能要用到

    (2)、toString()
        存放对象地址的哈希码值。
        返回一个对象的字符串表示形式。打印一个对象其实就是打印这个对象toString方法的返回值。
        可以覆盖类的toString()方法，从而打印我们需要的数据。 Public String toString(){……}

    (3)、equals(Object obj)
        用来判断对象的值是否相等。前提是覆盖了equals方法。Object类中的equals方法判断的依然是地址
        注意: String类已经覆盖了equals方法，所以能用equals来判断String对象的值是否相等。

        覆盖equals的原则:
            1.自反性(自己＝自己)
            2.对称性(y=x则x=y)
            3.一致性(多次调用，结果一致)
            4.传递性(A=B,B=C则A=C)。
        非空原则:  t1.equals(null) 返回 false (如果t1不等于空)

    (4)、clone() 克隆，拷贝
        一个对象参与序列化过程，那么对象流会记录该对象的状态，当再次序列化时，
        会重复序列化前面记录的对象初始状态，我们可以用对象克隆技术来解决这个问题
         1 类中覆盖父类的 clone 方法，提升 protected 为 public
         2 类实现 Cloneable 接口
        浅拷贝: 只简单复制对象的属性
        深拷贝: 如果被复制对象的属性也是一个对象,则还会复制这个属性对象
               这种复制是一个递归的过程,通过对象序列化实现


/******************** 覆盖equals方法的标准流程 ***************************/
  public boolean equals(Object obj){
    //第一步: 现判断两个对象地址是否相等
    if(this == obj)  return   true;
    //第二步: 如果参数是null的话直接返回false;
    if(obj == null)  return   false;
    //第三步: 如果两个对象不是同一个类型直接返回false
    if (getClass() != obj.getClass()) return false;
    //?? if(!(this.getClass.getName().equals(o.getClass.getName())) return false;
    //第四步: 将待比较对象强转成指定类型，然后自定义比较规则
       Student s = (Student) obj;
    if(s.name.equals(this.name)&&s.age==this.age) return true;
    else return false;
}
/*************************************************************************/

