部署描述符实际上是一个XML文件，包含了很多描述servlet/JSP应用的各个方面的元素，如servlet注册、servlet映射以及监听器注册。部署描述符从下面的XML头开始：
<?xml version="1.0" encoding="ISO-8859-1"?>
这个头指定了XML的版本号以及所使用的编码。头的下面是DOCTYPE声明：
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
这段代码指定文件类型定义(DTD)，可以通过它检查XML文档的有效性。下面显示的<!DOCTYPE>元素有几个特性，这些特性告诉我们关于DTD的信息：
●        web-app定义该文档(部署描述符，不是DTD文件)的根元素
●        PUBLIC意味着DTD文件可以被公开使用
●       "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"意味着DTD由Sun Microsystems, Inc.   
           维护。该信息也表示它描述的文档类型是DTD Web Application 2.3，而且DTD是用英文书写的。
●        URL"http://java.sun.com/dtd/web-app_2_3.dtd"表示D文件的位置。
注意：
在部署描述符中， <!--…-->用于注释。
部署描述符的根元素是web-app。DTD文件规定，web-app元素的子元素的语法如下：
<!ELEMENT web-app (icon?, display-name?, description?,
distributable?, context-param*, filter*, filter-mapping*,
listener*, servlet*, servlet-mapping*, session-config?,
mime-mapping*, welcome-file-list?,
error-page*, taglib*, resource-env-ref*, resource-ref*,
security-constraint*, login-config?, security-role*,env-entry*,
ejb-ref*, ejb-local-ref*)>
正如您所看到的，这个元素含有23个子元素，而且子元素都是可选的。问号(？)表示子元素是可选的，而且只能出现一次。星号(*)表示子元素可在部署描述符中出现零次或多次。有些子元素还可以有它们自己的子元素。

web.xml文件中web-app元素声明的是下面每个子元素的声明。下面的章节讲述部署描述符中可能包含的所有子元素。
注意：
在Servlet 2.3中，子元素必须按照DTD文件语法描述中指定的顺序出现。比如，如果部署描述符中的web-app元素有servlet和servlet-mapping两个子元素，则servlet子元素必须出现在servlet-mapping子元素之前。在Servlet 2.4中，顺序并不重要。
下面对web.xml文件各元素进行详解
1. icon元素
icon元素用来指定GIF格式或JPEG格式的小图标(16×16)或大图标(32×32)的文件名。
<!ELEMENT icon (small-icon?, large-icon?)>
<!ELEMENT small-icon (#PCDATA)>
<!ELEMENT large-icon (#PCDATA)>
icon元素包括两个可选的子元素：small-icon子元素和large-icon子元素。文件名是Web应用归档文件(WAR)的根的相对路径。
部署描述符并没有使用icon元素。但是，如果使用XML工具编辑部署描述符，XML编辑器可以使用icon元素。
2. display-name元素
如果使用工具编辑部署描述符，display-name元素包含的就是XML编辑器显示的名称。
<!ELEMENT display-name (#PCDATA)>
下面是一个含有display-name元素的部署描述符：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<display-name>Online Store Application</display-name>
</web-app>
3. description元素
可以使用description元素来提供有关部署描述符的信息。XML编辑器可以使用description元素的值。
<!ELEMENT description (#PCDATA)>
4. distributable元素
可以使用distributable元素来告诉servlet/JSP容器，编写将在分布式Web容器中部署的应用：
<!ELEMENT distributable EMPTY>
例如，下面是一个含有distributable元素的部署描述符的例子：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<distributable/>
</web-app>
5. context-param元素
context-param元素含有一对参数名和参数值，用作应用的servlet上下文初始化参数。参数名在整个Web应用中必须是惟一的。
<!ELEMENT context-param (param-name, param-value, description?)>
<!ELEMENT param-name (#PCDATA)>
<!ELEMENT param-value (#PCDATA)>
<!ELEMENT description (#PCDATA)>
param-name 子元素包含有参数名，而param-value子元素包含的是参数值。作为选择，可用description子元素来描述参数。
下面是一个含有context-param元素的有效部署描述符：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<context-param>
<param-name>jdbcDriver</param-name>
<param-value>com.mysql.jdbc.Driver</param-value>
</context-param>
</web-app>
6. filter元素
filter元素用于指定Web容器中的过滤器。在请求和响应对象被servlet处理之前或之后，可以使用过滤器对这两个对象进行操作。利用下一节介绍的filter-mapping元素，过滤器被映射到一个servlet或一个URL模式。这个过滤器的filter元素和filter-mapping元素必须具有相同的名称。
<!ELEMENT filter (icon?, filter-name, display-name?, description?,
filter-class, init-param*)>
<!ELEMENT filter-name (#PCDATA)>
<!ELEMENT filter-class (#PCDATA)>
icon、display-name和description元素的用法和上一节介绍的用法相同。init-param元素与context-param元素具有相同的元素描述符。filter-name元素用来定义过滤器的名称，该名称在整个应用中都必须是惟一的。filter-class元素指定过滤器类的完全限定的名称。
下面是一个使用filter元素的部署描述符的例子：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<filter>
<filter-name>Encryption Filter</filter-name>
<filter-class>com.branysoftware.EncryptionFilter</filter-class>
</filter>
</web-app>
7. filter-mapping元素
filter-mapping元素用来声明Web应用中的过滤器映射。过滤器可被映射到一个servlet或一个URL模式。将过滤器映射到一个servlet中会造成过滤器作用于servlet上。将过滤器映射到一个URL模式中则可以将过滤器应用于任何资源，只要该资源的URL与URL模式匹配。过滤是按照部署描述符的filter-mapping元素出现的顺序执行的。
<!ELEMENT filter-mapping (filter-name, (url-pattern | servlet-name))>
<!ELEMENT filter-name (#PCDATA)>
<!ELEMENT url-pattern (#PCDATA)>
<!ELEMENT servlet-name (#PCDATA)>
filter-name值必须对应filter元素中声明的其中一个过滤器名称。下面是一个含有filter-mapping元素的部署描述符：
<?xml version="1.0" encoding="ISO-8859-1">
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<filter>
<filter-name>Encryption Filter</filter-name>
<filter-class>com.brainysoftware.EncryptionFilter</filter-class>
</filter>
<filter-mapping>
<filter-name>Encryption Filter</filter-name>
<servlet-name>EncryptionFilteredServlet</servlet-name>
</filter-mapping>
</web-app>
8. listener元素
listener元素用来注册一个监听器类，可以在Web应用中包含该类。使用listener元素，可以收到事件什么时候发生以及用什么作为响应的通知。
<!ELEMENT listener (listener-class)>
<!ELEMENT listener-class (#PCDATA)>
下面是一个含有listener元素的有效部署描述符：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<listener>
<listener-class>MyAppListener</listener-class>
</listener>
</web-app>
9. servlet元素
servlet元素用来声明一个servlet。
<!ELEMENT servlet (icon?, servlet-name, display-name?, description?,
(servlet-class|jsp-file), init-param*, load-on-startup?, run-as?,
security-role-ref*)>
<!ELEMENT servlet-name (#PCDATA)>
<!ELEMENT servlet-class (#PCDATA)>
<!ELEMENT jsp-file (#PCDATA)>
<!ELEMENT init-param (param-name, param-value, description?)>
<!ELEMENT load-on-startup (#PCDATA)>
<!ELEMENT run-as (description?, role-name)>
<!ELEMENT role-name (#PCDATA)>
icon、display-name和description元素的用法和上一节介绍的用法相同。init-param元素与context-param元素具有相同的元素描述符。可以使用init-param子元素将初始化参数名和参数值传递给servlet。
(1) servlet-name、servlet-class和jsp-file元素
servlet元素必须含有servlet-name元素和servlet-class元素，或者servlet-name元素和jsp-file元素。描述如下：
●        servlet-name元素用来定义servlet的名称，该名称在整个应用中必须是惟一的。
●        servlet-class元素用来指定servlet的完全限定的名称。
●        jsp-file元素用来指定应用中JSP文件的完整路径。这个完整路径必须由a/开始。
(2) load-on-startup元素
当启动Web容器时，用load-on-startup元素自动将servlet加入内存。加载servlet就意味着实例化这个servlet，并调用它的init方法。可以使用这个元素来避免第一个servlet请求的响应因为servlet载入内存所导致的任何延迟。如果load-on-startup元素存在，而且也指定了jsp-file元素，则JSP文件会被重新编译成servlet，同时产生的servlet也被载入内存。
load-on-startup元素的内容可以为空，或者是一个整数。这个值表示由Web容器载入内存的顺序。举个例子，如果有两个servlet元素都含有load-on-startup子元素，则load-on-startup子元素值较小的servlet将先被加载。如果load-on-startup子元素值为空或负值，则由Web容器决定什么时候加载servlet。如果两个servlet的load-on-startup子元素值相同，则由Web容器决定先加载哪一个servlet。
(3) run-as元素
如果定义了run-as元素，它会重写用于调用Web应用中servlet所设定的Enterprise JavaBean(EJB)的安全身份。Role-name是为当前Web应用定义的一个安全角色的名称。
(4) security-role-ref元素
security-role-ref元素定义一个映射，该映射在servlet中用isUserInRole (String name)调用的角色名与为Web应用定义的安全角色名之间进行。security-role-ref元素的描述如下：
<!ELEMENT security-role-ref (description?, role-name, role-link)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT role-name (#PCDATA)>
<!ELEMENT role-link (#PCDATA)>
role-link元素用来将安全角色引用链接到已定义的安全角色。role-link元素必须含有已经在security-role元素中定义的一个安全角色的名称。
(5) Faces Servlet的servlet元素
在 JSF应用中，需要为Faces Servlet定义一个servlet元素，如下所示：
<?xml version="1.0"?>
<!DOCTYPE web-app PUBLIC
"-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<!-- Faces Servlet -->
<servlet>
<servlet-name>Faces Servlet</servlet-name>
<servlet-class>javax.faces.webapp.FacesServlet</servlet-class>
<load-on-startup> 1 </load-on-startup>
</servlet>
<!-- Faces Servlet Mapping -->
<servlet-mapping>
<servlet-name>Faces Servlet</servlet-name>
<url-pattern>/faces/*</url-pattern>
</servlet-mapping>
</web-app>
10. seervlet-mapping 元素
seervlet-mapping 元素将URL模式映射到某个servlet。
<!ELEMENT servlet-mapping (servlet-name, url-pattern)>
<!ELEMENT servlet-name (#PCDATA)>
<!ELEMENT url-pattern (#PCDATA)>
在前面的“servlet元素”一节中已经介绍了使用servlet-mapping元素的例子。
11. session-config元素
session-config元素为Web应用中的javax.servlet.http.HttpSession对象定义参数。
<!ELEMENT session-config (session-timeout?)>
<!ELEMENT session-timeout (#PCDATA)>
session-timeout元素用来指定默认的会话超时时间间隔，以分钟为单位。该元素值必须为整数。如果session-timeout元素的值为零或负数，则表示会话将永远不会超时。
下面是一个部署描述符，在用户最近访问HttpSession对象30分钟后，HttpSession对象默认为无效：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<session-config>
<session-timeout>30</session-timeout>
</session-config>
</web-app>
12. mime-mapping元素
mime-mapping元素将mime类型映射到扩展名。
<!ELEMENT mime-mapping (extension, mime-type)>
<!ELEMENT extension (#PCDATA)>
<!ELEMENT mime-type (#PCDATA)>
extension元素用来描述扩展名。mime-type元素则为MIME类型。
举个例子，下面的部署描述符将扩展名txt映射为text/plain：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<mime-mapping>
<extension>txt</extension>
<mime-type>text/plain</mime-type>
</mime-mapping>
</web-app>
13. welcome-file-list元素
当用户在浏览器中输入的URL不包含某个servlet名或JSP页面时，welcome-file-list元素可指定显示的默认文件。
<!ELEMENT welcome-file-list (welcome-file+)>
<!ELEMENT welcome-file (#PCDATA)>
举个例子说明，假设用户在浏览器的地址框中输入http://www.mycompany.com/appName/等地址。如果在Web应用的部署描述符中指定welcome-file-list元素，用户就会看到一个权限错误消息，或者是应用目录下的文件和目录列表。如果定义了welcome-file-list元素，用户就能看到由该元素指定的具体文件。
welcome-file子元素用于指定默认文件的名称。welcome-file-list元素可以包含一个或多个welcome-file子元素。如果在第一个welcome-file元素中没有找到指定的文件，Web容器就会尝试显示第二个，以此类推。
下面是一个包含welcome-file-list元素的部署描述符。该元素包含两个welcome-file元素：第一个指定应用目录中的main.html文件，第二个定义jsp目录下的welcom.jsp文件，jsp目录也在应用目录下。
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<welcome-file-list>
<welcome-file>main.html</welcome-file>
<welcome-file>jsp/welcome.jsp</welcome-file>
</welcome-file-list>
</web-app>
如果用户键入的URL不包含servlet名称、JSP页面或其他资源，则不会在应用目录中找到main.html文件，这时就会显示jsp目录下的welcome.jsp文件。
14. error-page元素
error-page元素用于将一段错误代码或一个异常类型映射到Web应用中的资源路径，从而在产生特殊的HTTP错误或指定的Java异常时，将显示相关的资源。
<!ELEMENT error-page ((error-code | exception-type), location)>
<!ELEMENT error-code (#PCDATA)>
<!ELEMENT exception-type (#PCDATA)>
<!ELEMENT location (#PCDATA)>
error-code元素包含HTTP错误代码。exception-type是Java异常类型的完全限定的名称。location元素是Web应用中的资源相对于应用目录的路径。location的值必须从a/开始。
举个例子，每次产生HTTP 404错误代码时，下面的部署描述符可使Web容器显示error404.html页面：
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE web-app
PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN"
"http://java.sun.com/dtd/web-app_2_3.dtd">
<web-app>
<error-page>
<error-code>404</error-code>
<location>/error404.html</location>
</error-page>
</web-app>
15. taglib元素
taglib元素描述JSP定制标记库。
<!ELEMENT taglib (taglib-uri, taglib-location)>
<!ELEMENT taglib-uri (#PCDATA)>
<!ELEMENT taglib-location (#PCDATA)>
taglib-uri元素是用于Web应用中的标记库的URI。taglib-uri元素的值与WEB-INF目录相对应。
taglib-location元素包含一个位置，其中可以找到标记库的标记库描述符(TLD)文件。
16. resource-env-ref元素
可以使用resource-env-ref元素来指定对管理对象的servlet引用的声明，该对象与servlet环境中的资源相关联。
<!ELEMENT resource-env-ref (description?, resource-env-ref-name,
resource-env-ref-type)>
<!ELEMENT resource-env-ref-name (#PCDATA)>
<!ELEMENT resource-env-ref-type (#PCDATA)>
resource-env-ref-name元素是资源环境引用的名称，其值为servlet代码中使用的环境的入口名称。该名称是一个与java:comp/env相对应的Java命名和目录接口(JNDI)名称，该名称在整个Web应用中必须是惟一的。
17. resource-ref元素
resource-ref元素用于指定对外部资源的servlet引用的声明。
<!ELEMENT resource-ref (description?, res-ref-name,
res-type, res-auth, res-sharing-scope?)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT res-ref-name (#PCDATA)>
<!ELEMENT res-type (#PCDATA)>
<!ELEMENT res-auth (#PCDATA)>
<!ELEMENT res-sharing-scope (#PCDATA)>
resource-ref子元素的描述如下：
●        res-ref-name是资源工厂引用名的名称。该名称是一个与java:comp/env上下文相对应的JNDI名称，并且在整个Web应用中必须是惟一的。
●        res-auth表明：servlet代码通过编程注册到资源管理器，或者是容器将代表servlet注册到资源管理器。该元素的值必须为Application或Container。
●        res-sharing-scope表明：是否可以共享通过给定资源管理器连接工厂引用获得的连接。该元素的值必须为Shareable(默认值)或Unshareable。
18. security-constraint元素
部署描述符中的security-constraint元素允许不通过编程就可以限制对某个资源的访问。
<!ELEMENT security-constraint (display-name?,
web-resource-collection+,
auth-constraint?, user-data-constraint?)>
<!ELEMENT display-name (#PCDATA)>
<!ELEMENT web-resource-collection (web-resource-name, description?,
url-pattern*, http-method*)>
<!ELEMENT auth-constraint (description?, role-name*)>
<!ELEMENT user-data-constraint (description?, transport-guarantee)>
(1) web-resource-collection元素
web-resource-collection元素标识需要限制访问的资源子集。在web-resource-collection元素中，可以定义URL模式和HTTP方法。如果不存在HTTP方法，就将安全约束应用于所有的方法。
<!ELEMENT web-resource-collection (web-resource-name, description?,
url-pattern*, http-method*)>
<!ELEMENT web-resource-name (#PCDATA)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT url-pattern (#PCDATA)>
<!ELEMENT http-method (#PCDATA)>
web-resource-name是与受保护资源相关联的名称。http-method元素可被赋予一个HTTP方法，比如GET和POST。
(2) auth-constraint元素
auth-constraint元素用于指定可以访问该资源集合的用户角色。如果没有指定auth-constraint元素，就将安全约束应用于所有角色。
<!ELEMENT auth-constraint (description?, role-name*)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT role-name (#PCDATA)>
role-name元素包含安全角色的名称。
(3) user-data-constraint元素
user-data-constraint元素用来显示怎样保护在客户端和Web容器之间传递的数据。
<!ELEMENT user-data-constraint (description?, transport-guarantee)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT transport-guarantee (#PCDATA)>
transport-guarantee元素必须具有如下的某个值：
●        NONE，这意味着应用不需要传输保证。
●        INTEGRAL，意味着服务器和客户端之间的数据必须以某种方式发送，而且在传送中不能改变。
●        CONFIDENTIAL，这意味着传输的数据必须是加密的数据。
在大多数情况下，安全套接字层(SSL)用于INTEGRAL或CONFIDENTIAL。
19. login-config元素
login-config元素用来指定所使用的验证方法、领域名和表单验证机制所需的特性。
<!ELEMENT login-config (auth-method?, realm-name?,
form-login-config?)>
<!ELEMENT auth-method (#PCDATA)>
<!ELEMENT realm-name (#PCDATA)>
<!ELEMENT form-login-config (form-login-page, form-error-page)>
login-config子元素的描述如下：
●        auth-method指定验证方法。它的值为下面的一个：BASIC、DIGEST、FORM或 CLIENT-CERT
●        realm-name指定HTTP Basic验证中使用的领域名。
●        form-login-config指定基于表单的登录中应该使用的登录页面和出错页面。如果没有使用基于表单的验证，则忽略这些元素。这个元素的定义如下，其中form-login-page用于指定显示登录页面的资源路径， form-error-page则用于指定用户登录失败时显示出错页面的资源路径。这两个页面路径都必须以a/开始，并与应用目录相对应。
<!ELEMENT form-login-config (form-login-page, form-error-page)>
<!ELEMENT form-login-page (#PCDATA)>
<!ELEMENT form-error-page (#PCDATA)>
20. security-role元素
security-role元素指定用于安全约束中的安全角色的声明。
<!ELEMENT security-role (description?, role-name)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT role-name (#PCDATA)>
21. env-entry元素
env-entry元素用于指定应用环境入口。
<!ELEMENT env-entry (description?, env-entry-name, env-entry-value?,
env-entry-type)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT env-entry-name (#PCDATA)>
<!ELEMENT env-entry-value (#PCDATA)>
<!ELEMENT env-entry-type (#PCDATA)>
env-entry-name元素包含Web应用环境入口的名称。该名称是一个与java:comp/env相对应的JNDI名称，并且在整个应用中必须是惟一的。
env-entry-value元素包含Web应用环境入口的值。该值必须是一个字符串类型的值，并且对于指定类型的构造函数是有效的，该函数获得一个String参数；或者对于java.lang.Character是有效的，java.lang.Character对象是一个字符。
env-entry-type元素包含环境入口值的完全限定的Java类型，该环境入口值是Web应用代码所期望的。这个env-entry-type元素的值必须是如下之一：
java.lang.Boolean
java.lang.Byte
java.lang.Character
java.lang.String
java.lang.Short
java.lang.Integer
java.lang.Long
java.lang.Float
java.lang.Double
22. ejb-ref元素
ejb-ref元素用于指定EJB的home接口的引用。
<!ELEMENT ejb-ref (description?, ejb-ref-name, ejb-ref-type, home,
remote, ejb-link?)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT ejb-ref-name (#PCDATA)>
<!ELEMENT ejb-ref-type (#PCDATA)>
<!ELEMENT home (#PCDATA)>
<!ELEMENT remote (#PCDATA)>
<!ELEMENT ejb-link (#PCDATA)>
ejb-ref-name包含EJB引用的名称。EJB引用是servlet环境中的一个入口，它与java:comp/env相对应。这个名称在Web应用中必须是惟一的。为求一致性，推荐您的ejb-ref-name元素名称以ejb/开始。
ejb-ref-name元素包含引用的EJB的期望类型。这个值必须是Entity或Session。
home元素包含EJB的home接口的完全限定的名称。remote元素包含EJB的remote接口的完全限定的名称。
ejb-ref或ejb-local-ref元素中用到的ejb-link元素可指定EJB 引用被链接到另一个EJB。Ejb-link元素的值必须是同一个J2EE应用单元中某个EJB的ejb-name。Ejb-link元素中的名称可以由指定ejb-jar的路径名组成，该ejb-jar包含引用的EJB。目标bean的名称添加在后面，用字符a# 与路径名分隔。路径名与包含引用EJB的Web应用的WAR相对应。这就允许我们惟一标识具有相同ejb-name的多个企业bean。
23. ejb-local-ref元素
ejb-local-ref元素用于声明对EJB的本地home的引用。
<!ELEMENT ejb-local-ref (description?, ejb-ref-name, ejb-ref-type,
local-home, local, ejb-link?)>
<!ELEMENT description (#PCDATA)>
<!ELEMENT ejb-ref-name (#PCDATA)>
<!ELEMENT ejb-ref-type (#PCDATA)>
<!ELEMENT local-home (#PCDATA)>
<!ELEMENT local (#PCDATA)>
<!ELEMENT ejb-link (#PCDATA)>
local元素包含EJB本地接口的完全限定的名称。Local-home元素包含EJB本地home接口的完全限定的名称。

