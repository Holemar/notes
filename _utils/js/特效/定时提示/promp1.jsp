<%@ page import="java.util.*" contentType="text/xml;charset=utf-8"%>
<%
	String s1 = "下午来开会";
	String s2 = "你被开除了";
	String s3 = "为什么是我啊？";
	String s4 = "谁让你往枪口上撞？";
	response.setContentType("text/xml");
	response.setHeader("Cache-Control", "no-cache");
	//   List list = (List)request.getAttribute("messages");    
	out.println("<messages>");

	out.println("<message>");
	out.println("<id>" + 1 + "</id>");
	out.println("<title>" + s1 + "</title>");
	out.println("</message>");
	out.println("<message>");
	out.println("<id>" + 2 + "</id>");
	out.println("<title>" + s2 + "</title>");
	out.println("</message>");
	out.println("<message>");
	out.println("<id>" + 3 + "</id>");
	out.println("<title>" + s3 + "</title>");
	out.println("</message>");
	out.println("<message>");
	out.println("<id>" + 4 + "</id>");
	out.println("<title>" + s4 + "</title>");
	out.println("</message>");
	out.println("</messages>");
	
%>

