---
title: "BinQL: a CodeQL extension for binary formats"
source: "Thalium"
url: https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/
published: 2026-11-13
fetched: 2026-11-16T22:15:04.746781+08:00
category: "杂项"
score: 3.2
keywords: ["novel", "firmware"]
sha256: aad64a4a280aa50772930e9e851eb83586a24b735309c526df260b1a8d86a289
bytes: 50252
truncated: false
body_mode: fulltext
status: published
published_at: 2026-11-16T22:16:27.064129+08:00
---

# BinQL: a CodeQL extension for binary formats

> 来源：Thalium · 2026-11-13 · [原文](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/)
> 自动抓取快照，仅供安全研究参考；版权归原作者所有。

## 收录理由

- **核心**：逆向 CodeQL 的未公开组件（extractor、专有数据库格式），把它们重新实现到二进制上，做出 BinQL——让 CodeQL 对编译产物（无源码的固件）也能做“变体搜索”。
- **价值**：漏洞变体挖掘（variant analysis）从源码扩展到二进制，对闭源固件/设备固件尤其关键：找到一个洞之后，同类解析逻辑的其他洞往往只差一次查询。
- **难度**：很高。需要同时啃编译器 IR、CodeQL schema 与二进制格式解析。

# BinQL: a CodeQL extension for binary formats

Once a vulnerability is found, its variants are rarely far behind, and finding them is tedious, repetitive work. CodeQL solved this for source code by making a codebase queryable. No equivalent existed for the binaries reverse engineers actually work on.

This post details the reverse engineering of CodeQL’s undocumented components, its extractors and proprietary formats, and their reimplementation for binaries in BinQL, a tool that makes CodeQL as effective on compiled code as on C/C++, whether to hunt variants, track a bug across versions, or shortlist exploit candidates.

We also presented this work at GreHack 2026, on November 13, 2026.

## Table of Contents

- Context
- State of the Art
  - Tools that work with source code
  - Grep
- Semgrep
- CodeQL
- Tools that work with binaries
  - Hexrays toolbox
- rev.ng
- CodeQL: Also a Powerful Binary Analysis Engine
- Conclusion
- CodeQL internals
  - From the high up
- Extractor engine
  - Extractor and `autobuild` mechanism
- Extractor core
- .DBSCHEME file
- TRAP files
- Query engine
  - Standard library
- Query compiler & Evaluator
- Result
- Building an extractor for binary formats
  - Key principles
- Compiler core choice
  - IDA’s lifting pipeline
- IDA’s Ctree
- Designing the .DBSCHEME file
- Building a QL standard library for binaries
- Usage
  - Use it in practice
- Benchmark
- Use cases
  - Find a vulnerable bundled library
- Enumerate UAF heap-spray candidates
- Conclusion
  - Future work
- Gaining Traction for humans and LLM
- In the age of AI
- Last words

# Context

Vulnerabilities tend to cluster rather than occur in isolation: once one becomes a public 1-day, the same class tends to resurface wherever the same idiom, or the same author’s habits are repeated across a codebase. Variant analysis is therefore not a recent invention. Reviewers have practiced it implicitly for long: by hand at first, re-reading neighbouring code after every fix on the assumption that a mistake made once is rarely made only once, then increasingly with tooling, from a targeted grep to today’s static analysis engines.

Big Sleep, credited with finding real-world 0-days through automated variant hunting, put the same idea into words:

> This was a previous bug; there is probably another similar one somewhere.
> The Big Sleep Team

# State of the Art

The following is a non-exhaustive overview of publicly available static analysis tools.

## Tools that work with source code

When the source is available, three tools cover the spectrum from quick-and-dirty to fully expressive, in increasing order of power: grep, Semgrep, and CodeQL.

### Grep

The simplest tool is also the oldest: grep. It is cheap, fast, available everywhere, and matches raw text with regular expressions. To find calls to vuln_func with 23 as the first argument, a single pattern does the job:

```
grep

-En

'vuln_func\s*\(\s*23\b'
 *.c
```

That is also where it stops. grep works with characters and doesn’t understand code: it has no notion of a function call, an argument, a type or a scope. The pattern above already breaks on a line split across two lines, on a 23 reached through a macro or a constant, or on vuln_func appearing in a comment. Anything structural, “the first argument”, “a call reachable from main”, “a value that flows into this sink”, is out of reach. It is the right tool for a quick look, and the wrong one as soon as the question has structure.

### Semgrep

Semgrep operates on source code using pattern-matching rules written in YAML. It integrates seamlessly into CI/CD pipelines, catching issues early in a project’s development, such as hardcoded secrets (API keys, passwords), calls to dangerous functions (strcpy, system), weak cryptography (MD5, SHA-1). Unlike grep, it parses the code, so a rule matches syntax rather than text. The rule below flags every call to vuln_func:

```
-
id
:
vulnerable-call

pattern
:
vuln_func(...)

message
:
Suspicious Call

languages
:

  -
c

severity
:
ERROR
```

pattern: vuln_func(...) matches a call to vuln_func with any arguments (the ... is an argument wildcard), wherever it appears and however the source is formatted, without the false matches a grep would hit in comments or strings.

But this is also where Semgrep stops. It can match the shape of code, yet it struggles to express richer conditions: “the first argument is the literal 23”, “the call is reachable from main”, or “a tainted value flows into this argument”. It has no real notion of data flow across functions, so anything beyond local structural matching quickly becomes awkward or impossible.

### CodeQL

CodeQL, developed by Semmle (founded in 2006) and acquired by GitHub in 2019, is best described as SQL for source code. Its queries are written in QL, a declarative, object-oriented language compiling to Datalog, where classes are logical properties describing sets of values. This enables concise queries built on reusable libraries, scaling to codebases of millions of lines.

```
import

cpp

from

FunctionCall

call
,
Literal

lit

where

call
.
getTarget
().
getName
() =
"vuln_func"

and
 ...

select

call
,
"Suspicious call"
```

Beyond structural matching, CodeQL ships built-in data flow and taint tracking: you declare sources and sinks, and the engine finds the paths between them, following a value through assignments, calls and pointers (data flow), or through the data derived from it such as arithmetic and copies (taint tracking).

Data flow (solid) and taint tracking (dashed), from source to sink.

In order to build a database, source code access is mandatory, as is the associated build chain that builds the project. Historically, the C/C++ extractor gained a build-mode: none mode in v2.21.4 (May 2025) that relaxes the working-build requirement, though the source is still needed.

C/C++ extraction: a build tracer (LD_PRELOAD) feeds compiler contexts to CodeQL.

CodeQL is a well-adopted tool for finding needles in a haystack, pinpointing patterns of interest concealed across hundreds of thousands to millions of lines of code, from Windows drivers since 25H2 (2021), Chrome (Nov. 2024), Linux Kernel, Redis, FFmpeg (Oct. 2025), to Google, Elastic, OpenSearch, Wire, XStream (June 2026), etc&mldr;

Grep, Semgrep and CodeQL are powerful in increasing order of expressiveness, but they all share one hard requirement: source code. The moment the target is a stripped binary, a firmware image, a driver or a closed-source app, none of them apply. So how do we get the same pattern-matching leverage when all we have is the compiled artefact? To close this gap we sucessfully pushed CodeQL further into the territory of binaries and black-box targets.

## Tools that work with binaries

When there is no source, a handful of projects try to pattern-match on the binary itself, each taking a different route to get there.

### Hexrays toolbox

If you would rather not leave your decompiler and still want to match patterns, IDA Pro has Hexrays Toolbox: a collection of IDAPython scripts, untouched since November 2021, that find code patterns directly within IDA’s ctree.

Hex-Rays Toolbox matches patterns on the ctree

In practice it is not pleasant to use. A pattern is a hand-written Python predicate poking at raw ctree item kinds (cot_call, cot_asg, cot_obj, &mldr;): verbose, hard to read, and nothing like a query language. Worse, a mistake in that predicate tends to fail silently rather than raise a usable error, so you are left guessing why a match never fires. It works, but every non-trivial pattern is a chore, and that’s exactly the friction a proper query language is meant to remove.

### rev.ng

At REcon 2024, Path of Rev.ng: From Raw Bytes to CodeQL on Decompiled Code (slide 18) showcases how rev.ng (partially open-source but the product remains in closed beta) lifts binaries into compilable C, then feeds it into the CodeQL C/C++ extractor. Because the lifted output diverges from the original binary, its practical value for vulnerability research, pattern recognition, or binary navigation is limited.

### CodeQL: Also a Powerful Binary Analysis Engine

At Black Hat USA 2023, “CodeQL: Also a Powerful Binary Analysis Engine” gives a solid overview of CodeQL’s inner workings and proposes extending it to binaries. Two limitations, acknowledged in the talk itself, held it back.

First, it models the disassembly: the database and queries are expressed over x86 instructions. In practice nobody wants to write queries against assembly: a pattern that is one line of C becomes a brittle sequence of instruction matches, and the result is tied to one calling convention and optimization level. Pseudocode, not assembly, is the level reverse engineers actually prefer to reason at.

Second, being x86-specific makes the extractor expensive to maintain: every architecture (ARM, MIPS, &mldr;) would need its own instruction model, and each has to track the disassembler’s quirks. A decompiler-level representation sidesteps this, since the C AST is largely architecture-independent.

On top of that, the tool was never released publicly despite the slides stating otherwise, so none of it could be reused.

The Black Hat USA 2023 approach (slide 22/41)

## Conclusion

None of the three binary approaches is fully satisfying. Hex-Rays Toolbox matches on the ctree but is unmaintained and painful to write patterns for. rev.ng reuses CodeQL, yet on lifted C that no longer matches the real binary, so results are hard to map back. The Black Hat 2023 work explored the idea we build on, bringing CodeQL’s query engine to binaries, but it stopped at an x86 disassembler (matching assembly, not decompiled code) and was never released, therefore we decided to keep this direction.

The absence of a variant-analysis tool on decompiled code, together with CodeQL’s wide adoption, is what sparked our interest: could CodeQL be pushed further, into binaries and black-box targets? Answering that starts with understanding how CodeQL works under the hood.

# CodeQL internals

Extending CodeQL to binaries means reimplementing part of its machinery, so we first need to see how that machinery is put together.

## From the high up

At a high level, CodeQL runs in two stages. First, an extractor ingests the source code and emits a relational database that captures the code as data. Then, independently, the query engine takes your queries and runs them against that database to produce results.

CodeQL at a glance: extractor builds the `.rel` database, query engine runs queries on it.

The split matters: extraction happens once per codebase, and from then on any number of queries run against the database without ever touching the original code again. The sections below open up each stage, since building BinQL means reimplementing the first one and reusing the second.

## Extractor engine

The extractor engine is the front half of CodeQL: it turns code into the relational database everything else queries. This is the part BinQL has to reimplement, so it is worth a close look.

### Extractor and autobuild mechanism

When creating a database with codeql database create <database_path> --language=<lang> --command="<cmd>", the --command flag specifies how to compile the project before extraction.

Since binaries require no compilation, omitting --command causes CodeQL to invoke tools/autobuild.{cmd,sh}, which sets up the database directory structure and begins extraction (i.e., emitting TRAP files, which we detail in the TRAP files section).

CodeQL’s supported languages are neatly organized within the CodeQL distribution bundle:

```
/path/to/unzipped/
codeql-bundle-vx.y.z

├──
cpp/

├──
csharp/

├──
go/

└── ...
```

Registering a new binary language requires dropping a specifically structured, yet undocumented, directory alongside them:

```
/path/to/unzipped/codeql-bundle-vx.y.z/.../
binary

├─ codeql-extractor.yml
# Extractor configuration

├─ <extractor-name>.dbscheme
# Table definitions

├─ <extractor-name>.dbscheme.stats
# Required, purpose unknown

├─
tools

# Automation scripts

│  ├─ autobuild.sh
(on Linux)

│  └─ autobuild.cmd
(on Windows)

├─
qlpack

│  ├─
0.0.1

│  │  ├─ qlpack.yml
│  │  ├─ <extractor-name>.dbscheme
# Table definitions

│  │  ├─ <extractor-name>.dbscheme.stats
# Required, purpose unknown

│  │  ├─ <extractor-name>.qll
# Standard query library

│  │  └─
upgrades/initial/
<extractor-name>.dbscheme
│  └─ other versions ...
└─
extractor

# Python / any lang scripts
```

Every language the bundle ships lives in its own directory next to the others (cpp/, go/, &mldr;). BinQL adds its own entry, thalium/binary/, with the exact same internal layout, and the CodeQL engine then treats binary like any first-party language. Three pieces carry the registration:

- codeql-extractor.yml is the extractor manifest the engine reads first. It declares the language name (binary), points to the autobuild script that kicks off extraction, and lists the column-type aliases the DBSCHEME depends on.
- qlpack.yml turns each qlpack/<version>/ directory into a CodeQL pack, which is what the query engine resolves import binary against. It names the pack, its version, and the DBSCHEME the queries bind to.
- extractor/ is the extractor itself: the scripts (Python here, though any language works) that the autobuild script invokes to walk the binary and emit TRAP files.

### Extractor core

The extractor is implemented in Python, targeting IDA Pro 9.0+ to leverage idalib, IDA’s headless library interface, along with the improved developer-friendly API introduced in recent releases. It utilizes the following passes to produce TRAP files:

- The Binary pass collects all known global names (non-function symbols and data labels), then iterates over every function in the binary to emit function TRAP entries via the function pass.
- The Function pass performs per-function analysis in three phases:

  - type generation (emitting TRAP entries for local variable and parameter types),
- global variable discovery (scanning the function body for global accesses),
- ctree traversal (walking the decompiled AST to emit statement and expression TRAP entries).

Decompilation failures and unexpected exceptions are logged and skipped so a single bad function does not abort the binary extraction.

The binary pass drives the function pass: type generation, global discovery, then ctree traversal.

Since an extractor is simply software that emits TRAP files, and the DBSCHEME has been designed to be decompiler-agnostic, porting BinQL to other state-of-the-art, industry-standard decompilers is feasible.

### .DBSCHEME file

Any CodeQL journey starts with a DBSCHEME, defining the structure of the database queried. Its basic building block is a table declaration, identified by its name (by convention, plural):

```
locations
(

int

id
:
@location
,

string

binary
:
string

ref
,

float

start
:
float

ref
,

float

end
:
float

ref

)

functions
(

unique int

id
:
@function
,

string

name
:
string

ref
,

int

location
:
@location

ref

)

@ens_types
 =
@ens_primitive_types
 |
@ens_database_types
;
```

A column is written <type> <name>: <type> [ref]. Its type is either a primitive (int, bigint, string, boolean, float) or a @-prefixed database type. A primitive column is treated as a foreign key, and the ref suffix marks a reference into another table. The optional unique modifier, combined with a @ type, declares the table’s primary key:

```
unique int

id
:
@function
```

@ens_types is a type union, an alias grouping multiple @ types into database types referenceable as a single column type. A case statement goes further and turns a tagged column into a proper enumeration, dispatching a @-type per value:

```
instructions
(

unique int

id
:
@instruction
,

int

kind
:
int

ref

);

case

@instruction
.
kind

of

1
 =
@call

|
2
 =
@store

;
```

Two rules are easy to miss and will make extraction fail otherwise:

- the schema must declare a sourceLocationPrefix(string prefix: string ref) table, even when no TRAP entry is ever emitted for it.
- column types bind strictly, so an address that overflows a 32-bit int has to be declared bigint (see the Designing the .DBSCHEME file section).

That is the whole vocabulary: with tables, primitive and @ types, unique keys, ref, unions and case, you can model any AST.

### TRAP files

An extractor picks up artefacts during compilation, such as functions, variables, types, and function calls, and translates them into TRAP entries that populate the database.

```
location
(
1
,
"binary"
,
1234.0
,
5678.0
)

function
(
2
,
"main"
,
1
)
```

Each line is one row in the table named first, with the columns in DBSCHEME order. The two above read as: location 1 spans [1234, 5678) in the binary, and function 2 is named main and sits at location 1. Entries reference each other by id, exactly like foreign keys, so richer facts are built by chaining rows:

```
location
(
1
,
"binary"
,
1234.0
,
5678.0
)

function
(
2
,
"main"
,
1
)
# function is located at 1

variable
(
7
,
"argc"
,
2
)
# local var of function 2

funcall
(
9
,
2
,
15
)
# function 2 calls callee 15

expr
(
31
,
9
,
"0x1337"
)
# constant expression inside call 9
```

Walking the source AST, the extractor emits one such row per node it recognises, and the whole codebase ends up expressed as a handful of flat, cross-referencing tables.

The ids above are shown as plain integers for readability, but TRAP also lets you define them through labels, and that is what the official C/C++ extractor does. A row is a tuple tupleName(arg1, arg2, ...), and a label is written #label, bound with #label = <value> and referenced by name wherever that id is needed. Three values are accepted:

- *: allocate a fresh, guaranteed-unique key automatically.
- @"<KEY>": bind an explicit key you choose (handy to give the same entity a stable id and deduplicate it across TRAP files).
- #other: copy the value of an already-bound label.

So the chained rows above are really emitted as:

```
#main
 = *

functions
(
#main
,
"main"
,
#loc
)

#argc
 = *

variable
(
#argc
,
"argc"
,
#main
)
// references the function's label
```

Labels let the extractor emit rows in any order without tracking numeric ids itself, and @"..." keys let independently-generated TRAP files agree on the same entity. The importer resolves every label to a concrete id when loading the database.

Once all TRAP files are emitted, CodeQL takes back control from the extractor and validates them against three criteria: syntax (unmatched delimiters, unterminated strings), semantics (uniqueness constraints, arity, type coercion) and compliance against the language’s DBSCHEME. Errors at this stage are descriptive enough to trace back to the relevant extractor code.

The engine then converts the validated TRAP into REL binary files (.rel), the actual relational, set-based representation of the database. From there it is ready to use via the CLI, the CodeQL VSCode extension or any other CodeQL-compatible tooling.

## Query engine

Once the database exists, the query engine is the back half that runs queries against it. BinQL reuses this part mostly unchanged, but understanding it explains what a query actually does to the extracted data.

### Standard library

Nobody queries the raw database directly. A table like functions(id, name, type, location) is efficient for the engine but a nightmare to write queries against: every query would have to know each table’s column order and join them by hand.

Each CodeQL language therefore ships a standard library, a set of .qll files that wrap those tables in an object-oriented API. A row of functions becomes a Function object, its columns become accessors (getName(), getType(), getLocation()), and recurring patterns become reusable predicates (hasName(...)). On top of this base sit the higher-level libraries CodeQL is known for, most notably its data flow analysis, all expressed in the same QL language.

The payoff is that a query reads at the level of the code, not the schema: you write from Function f where f.hasName("malloc") instead of joining relations by id. The library is what makes CodeQL feel like “SQL for code” rather than raw Datalog, and reproducing it for binaries is exactly what the Building a QL standard library for binaries section is about.

### Query compiler & Evaluator

Querying a database never involves the extractor again. The query compiler lowers the high-level QL into something the engine can evaluate, through two successive lowering phases[1](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/#fn:1):

- QL → DIL. The .ql/.qll source, together with the standard libraries it imports and the database schema, is first lowered to DIL (Datalog Intermediate Language): the declarative from/where/select logic becomes nested Datalog-style predicate clauses. The compiled query modules are cached as `.qlx` files (the compilation cache), so an unchanged query skips recompilation on the next run.
- DIL → RA. DIL is lowered again to RA (Relational Algebra): the low-level operations the evaluator actually runs: classic JOIN, UNION and boolean set operations over relations.

In short, the query is lowered twice before anything runs, then executed by the evaluator:

Query execution: QL is lowered to DIL then RA, run against the `.rel` database to yield BQRS results.

The evaluator (core engine) then runs the RA program against the .rel relations. Intermediate predicate results are written to an evaluation cache inside the database directory (db-<lang>/default/cache/), so a later query that builds on an already-computed predicate reuses it instead of recomputing: compute a set A once, and a query that filters it with new where constraints into a subset B of A reuses A rather than rebuilding it. The final relation is returned as a BQRS (Binary Query Result Set) and rendered as a table in the CLI or the VS Code extension, each row linking back to the matching location.

Full pipeline: extractor to TRAP to importer to `.rel` database, then query engine to results.

Now that we have a better understanding of the various files involved in a CodeQL database, implementing a CodeQL extractor will be easier.

### Result

All of that machinery, extractor, DBSCHEME, TRAP, importer, query compiler and evaluator, exists so that the end result is dead simple to use. In practice a CodeQL user never sees any of it: they write a query on one side and read a table of matches on the other.

The user’s view: a query on the left, a structured results table on the right.

The query above describes code, without going through the underlying abstraction: from FunctionCall call, Literal lit ranges over the classes the standard library exposes, and the where clause states the pattern. Running it returns a table where each row is a match, linking back to the exact location. Everything covered in this section, the schema, the TRAP files, the two lowering phases, the caches, runs behind that single interface.

This is exactly the experience we want to bring to binaries. The rest of the article builds a binary extractor and library so that the same from ... where ... select ... workflow applies to a stripped binary, with import binary in place of import cpp.

# Building an extractor for binary formats

To implement an extractor we must comply with undocumented prerequisites[2](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/#fn:2).

> There is no official support for third-party extractors at this point in time.
> That doesn’t mean you cannot implement one.
> Remco Vermeulen, a staff CodeQL analysis engineer at GitHub, on adding support for the Dart language, Oct. 2024

By inspecting the official C/C++ extractor and a third-party one for Kaleidoscope, we uncovered enough undocumented prerequisites to build an extractor the CodeQL engine accepts.

The rest of this section walks through building one, from the files that spark extraction to the standard library a reverse engineer actually uses.

## Key principles

Three principles guided every design decision in BinQL:

- Architecture-agnostic. The schema and the queries make no assumption about the target CPU, so x86, ARM, MIPS and the rest all go through the same pipeline. One representation to maintain instead of one per architecture keeps the maintenance cost down.
- Return the binary’s data as-is. The extractor reports what the decompiler actually produced, without normalising or second-guessing it. Preserving the original code faithfully is what lets a query reason about the real binary rather than an idealised version of it.
- Use it like C/C++, but on binaries. The library mirrors CodeQL’s C/C++ model, so anyone already fluent in CodeQL is immediately productive: in the best case, swapping import cpp for import binary is all it takes.

## Compiler core choice

“CodeQL: Also a Powerful Binary Analysis Engine” proposed using SOTA disassemblers to populate the database. However, expressing patterns in assembly when decompilers are available feels like a regression: you would rather hit F5 in IDA and grep the output.

The question is then to determine which reprensentation to pick that would fit the pattern matching on binaries.

There are three standard decompilers on the market:

- Binary Ninja, a commercial decompiler with a free tier, which exposes a stack of intermediate languages but no one in the team uses it.
- Ghidra, on the other hand give an architecture agnostic intermediate representation, namme the P-Code produced by SLEIGH which is handy on exotic targets. It’s open-source and used by a part of our reversers.
- IDA Pro, the more expensive option of the three and the main decompiler at Thalium with an API we already know.

### IDA’s lifting pipeline

IDA does not jump straight from bytes to pseudocode. It works through a stack of representations, each one further from the raw instructions and closer to the C you end up reading. Following a single line back down that stack is the easiest way to see what is available to build on. Take:

```
int

res
 =
vuln_func
(
23
,
input
);
```

Assembly. The starting point, specific to the CPU architecture:

```
lea
   rax, [rbp+input]

mov
   rsi, rax

mov
   edi,
539h

call

vuln_func

mov
   [rbp+res], eax
```

Microcode. IDA lifts the assembly to microcode, its own intermediate representation, which is architecture-agnostic. Everything that follows operates on microcode, which IDA refines through several maturity levels:

```
mov

#0x539
.4, edi.4

mov
   &(%input).8, rsi.8

call

$vuln_func

<fast:int edi.4, char * rsi.8>.4

// prototype inferred by IDA

mov
   eax.4, %res.4
```

Ctree. From the matured microcode, IDA builds the ctree, a tree of statements that hold nested expressions:

```
expr

└
asg

  ├
var

res

  └
call

    ├
obj

vuln_func

    ├
num

23

    └
var

input
```

Pseudocode. The text you get when you press F5 is nothing more than the ctree printed to screen.

BinQL extracts the ctree. It is the closest thing to a C/C++ AST we can recover from a binary, which is precisely what lets us write queries the same way we would on source code.

### IDA’s Ctree

The ctree is exposed through IDA Pro’s SDK, natively in C++ and Python, and from Rust through the `idalib` bindings. Each node carries a kind that says which piece of C it represents, for instance any integer literal such as 0x12 becomes a cot_num node.

Our example line decomposes as follows. It is an expression statement (expr) that wraps a tree of expressions: an assignment (asg) whose left side is the variable res and whose right side is a call. The call targets the function vuln_func and carries two arguments, the number 23 and the variable input:

IDA ctree: an expression statement (blue) over typed expressions (grey).

In the end, a node boils down to three things: its kind (what piece of C it is), the data attached to it (the variable name, the literal value, the callee&mldr;), and its parent relationship (which node it hangs under, and in what order among its siblings). Those three ingredients, kind, data, and parentage, are exactly what we store in the database, and what makes the AST queryable the same way the C/C++ library is.

## Designing the .DBSCHEME file

We won’t walk through every table here, the full schema lives in the BinQL repository for anyone who wants the details. What matters is the three design choices behind it.

First, the schema deliberately mirrors CodeQL’s C/C++ schema: same shape of tables for functions, variables, types, calls and expressions. That is what makes principle 3 possible, a query written against C/C++ mostly transfers as-is.

Second, it stays decompiler-agnostic: nothing in the schema is specific to IDA or to Hex-Rays ctree. The tables describe a generic C AST, so a future Ghidra or Binary Ninja backend can populate the exact same database without schema changes.

Third, the schema is not just a subset of the C/C++ one, it also carries facts that only exist at the binary level and have no source equivalent: concrete addresses (the effective address of each function and instruction), and the symbol linkage of each function, whether it is imported from another module or exported to one. Conversely, source-only concepts with no binary meaning, such as file or line locations, are dropped. The net result is a schema close enough to C/C++ to reuse its queries, yet honest about what a binary actually exposes.

Storing those addresses raises a subtlety worth flagging: CodeQL’s primitive int is a signed 32-bit integer. That is fine for source code, where the numbers a query deals with are small, but an effective address (EA) on a 64-bit binary does not fit, 0x7fff_ffff is already the largest positive int, so importing any TRAP whose value exceeds it crashes the import. CodeQL’s answer is `bigint`, an arbitrary-precision integer type (no fixed width, it grows to hold whatever value you give it) added to the language precisely for cases like this. So in the binary schema, every column that holds an address, an offset, or a size is typed as bigint rather than int, and the library’s accessors (getEA(), getOffset(), &mldr;) return bigint. The cost is minor but present: a query comparing an EA to a literal has to write it as a bigint literal (0x1337.toBigInt() style) rather than a bare int, which is the one place C/C++ queries need adjusting when ported.

## Building a QL standard library for binaries

A CodeQL library for binaries&mldr;

Once artefacts are stored in REL files, a library written in .qll files in the QL language exposes the database through a set of classes providing predicates to query the underlying data.

Each class must implement a string toString() function and extend either a database type (@typename as described in the DBSCHEME) or another class.

Take the functions(id, name, type, location) table from the DBSCHEME: wrapping it in a class turns raw rows into an object with named accessors.

```
class

Function

extends

@function
 {

/**
   * Constructor predicate to bind this instance to known functions.
   */

Function
() {
functions
(
this
, _, _, _) }

/**
   * Gets the name of the function.
   */

string

getName
() {
functions
(
this
,
result
, _, _) }

/**
   * Holds if the Function has name `name`.
   */

predicate

hasName
(
string

name
) {
this
.
getName
() =
name
 }

/**
   * Gets the type of the function.
   */

Type

getType
() {
functions
(
this
, _,
result
, _) }

/**
   * Gets the source location of the function.
   */

Location

getLocation
() {
functions
(
this
, _, _,
result
) }

/**
   * Returns a string representation including the function name.
   */

string

toString
() {
result
 =
"Function "
 +
this
.
getName
() }
}
```

Reading it top to bottom:

- extends @function binds the class to the database type, so its instances are exactly the rows of the functions table.
- Function(), the characteristic predicate, constrains membership: functions(this, _, _, _) says “this value appears as an id in functions” (the _ wildcards ignore the other columns).
- the getters project a single column back out: getName() reads column 2, getType() column 3, getLocation() column 4, each unifying result with that slot.
- hasName(string name) is a convenience predicate built on top of a getter, the pattern most of the library is made of.
- toString() is mandatory and drives how a result is displayed in the query output.

From here, every other artefact (variables, calls, types, expressions) gets the same treatment: one class per table, getters mirroring its columns, plus a few extra methods for syntactic sugar.

&mldr; documented&mldr;

A reverse engineer working with a custom CodeQL library for binaries wants the same experience as the C/C++ standard library documentation: a browsable HTML reference, ideally available offline, of every module, class, predicate, member, and type.

When .qll files contain CodeQL’s docstring format, QLDoc, codeql generate library-doc generates an equivalent HTML reference from them[3](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/#fn:3).

&mldr; as if it were a C/C++ library

One of BinQL’s design constraints is making existing C/C++ queries reusable on binaries with as little friction as possible. Ideally, swapping import cpp for import binary is the only change required. In practice, the binary DBSCHEME diverges from its C/C++ counterpart wherever a concept has no binary equivalent (or vice versa), so some queries still need light adjustments.

```
diff --git a/cpp.ql b/binary.ql

--- a/cpp.ql

+++ b/binary.ql

-import cpp

+import binary

 from Function f

-where f.getFile().getBaseName() = "vulnerable_code.c"

+where f.getLocation().getStart() = 0x1337

 select f
```

Binaries can now be queried “as though they were data”[4](https://blog.thalium.re/posts/binql-a-codeql-extension-for-binary-formats/#fn:4): import binary, and let’s hunt for patterns!

# Usage

With the extractor and library in place, BinQL is usable end to end. This section covers how to run it and what it costs on real binaries.

## Use it in practice

Database generation currently supports Linux and macOS, however query execution is OS agnostic from the CLI or the CodeQL VScode extension. A valid IDA Pro license for the target architecture is required to run the decompiler, and therefore the BinQL extractor.

## Benchmark

However, extraction can be time-intensive on large binaries. Measured on an Intel i7-12700 running IDA Pro 9.4 sp1 with 64 GB of RAM:

Pulled from the internetSizeTime (decompilation + extraction)`libc.so` (Android 16, Bionic)1 MB1min`libobjc.A.dylib` (iOS 26.6.2, dyld cache)94 MB1min`kernel32.dll` (Windows 11 23H2)0.8 MB1min`ntdll.dll` (Windows 11 23H2)2.2 MB2min`CoreFoundation` (macOS 26.6.2, dyld cache)12 MB4min`kernelcache` (iOS 26.6.2, XNU core)12 MB16min`ntoskrnl.exe` (Windows 11 23H2)13 MB16min`kernelcache` (macOS 26.6.2, XNU core)15 MB18min`vmlinux` (Android 16 GKI, 6.12)466 MB1h`kernelcache` (iOS 26.6.2, XNU + kexts)69 MB1h 30min`kernelcache` (macOS 26.6.2, XNU + kexts)115 MB2h 30min

Compiled locallySizeTime (decompilation + extraction)`curl` (v8.20.0)0.9 MB1min`redis-server` (v7.4.1)2.8 MB2min`ffmpeg` (v7.1)3.2 MB5min`openssl` (v3.4.0)6.8 MB6min`vmlinux` (Linux 6.12.9)52 MB42min

Extraction is a one-off cost per binary. Every later query then runs against the .rel database in seconds, minutes at most. The extraction itself stays in the minute range for binaries (libraries, userland programs), which is perfectly usable, while whole kernels push it into the hours, so on those targets it is worth running once and reusing the database.

Binary size is an easy metric to eyeball, but it does not predict the cost: libobjc.A.dylib (94 MB) extracts in a minute while a 12 MB kernelcache takes sixteen. What actually drives the time is code density, the number of IDA functions and the number of ctree nodes in each, since most of the runtime goes into IDA’s decompilation.

# Use cases

The two cases below show the same tool from opposite ends of the vulnerability lifecycle: first chasing a known bug across many shipped builds, then helping shape an exploit for a bug that is already found. Both run the identical query interface whether or not source is available, which is the whole point of BinQL.

## Find a vulnerable bundled library

Applications routinely statically link third-party open-source libraries (zlib, libpng, freetype, openssl, curl, ffmpeg, &mldr;) straight into their binaries. Version tracking of those embedded copies is rarely automated, so a product can ship, for months or even years, a library that is several releases behind, long after a bug in it became a public 1-day. Finding which shipped builds still carry the vulnerable copy is exactly the kind of needle-in-many-haystacks search CodeQL is good at. That makes it a natural first use case.

Our target here is CVE-2018-25032, an out-of-bounds write in zlib’s deflate: affecting every version before 1.2.12, it lets a crafted input corrupt memory past the pending_buf/d_buf overlay region during compression. As zlib is open-source, we can start from the patch itself and work backwards to a query that matches the compiled code for that vulnerability.

We take the fix commit `5c44459c` to see how the patch was applied. One of the lines involved in the vulnerability is deflate.c:343, which the commit removes:

```
// deflate.c:343 — removed by commit 5c44459c

- s->d_buf = overlay + s->lit_bufsize/sizeof(ush);
```

The source code tells us what the bug is, but our targets are (possibly stripped) binaries, so our query has to match the compiler’s output. So we patch-diff the same function in IDA Pro to see what the pattern actually looks like once decompiled:

```
s->d_buf
 =
overlay
 + (
lit_bufsize
 &
0xFFFFFFFE
);
```

These are the same computation: overlay is a ush * (pointer to a 2-byte unsigned short), so the /sizeof(ush) on a byte address becomes a /2×2 that turns into & 0xFFFFFFFE, a classic compiler optimization, which is what the decompiler shows once the pointer type is gone.

We write the CodeQL query to match it:

```
import

binary

from

BitwiseAndExpr

mask
, [...]

where

  [...]
and

mask
.
getRightChild
().
getHexValue
() =
"0xFFFFFFFE"

select

add
,
add
.
getEA
(),
"overlay + (lit_bufsize & 0xFFFFFFFE)"
```

The snippet above is trimmed for readability: matching the & 0xFFFFFFFE mask alone fires on far too much code, since it is a common compiler optimization pattern. The reproducible method is to start from that one anchoring constraint and tighten iteratively until only the vulnerable pattern survives, each extra where clause ruling out a class of false positives:

- anchor on the most specific literal from the patch (here the 0xFFFFFFFE mask).
- constrain the surrounding context the mask has to feed an addition, mirroring overlay + lit_bufsize / sizeof(ush).
- constrain the calling context, the expression lives inside the deflate-family function the patch touched, matched by its call graph or nearby string/constant fingerprints rather than by name, which is stripped.
- check the hit count against a known-vulnerable and a known-fixed build, and keep tightening until the fixed build returns nothing.

The same recipe transfers to any patch: pin the most distinctive compiled artefact of the fix, then add structural constraints until the query separates vulnerable from patched.

Pointed at the zlib copies bundled in two widely deployed Android readers, our query (with the additional constraints above) pinned down CVE-2018-25032 per version:

- Foxit PDF: v11.0.2 and v12.0.2 are vulnerable, while v2024.5.0 and v2024.11 are fixed.
- Adobe Reader: v21.1 and v22.1 are vulnerable, while v23.1 and v24.1 are patched.

Nothing about this is specific to two readers. The same query runs unchanged over any binary that bundles zlib, so the natural next step is to drive it at scale:

- build a corpus of binaries (e.g. APKs or firmware images) that embed the zlib library.
- generate a CodeQL database for each.
- run the query across every database.
- triage the hits, narrowing them down to a human-reviewable list.

## Enumerate UAF heap-spray candidates

Turning a use-after-free into a usable primitive hinges on reclaiming the freed slot with an object the attacker controls, and finding that replacement object is the tedious part of the work.

Modern allocators make it harder:

- they segregate allocations by size, so only an object that lands in the same size range as the freed one can reoccupy the slot.
- the useful primitive usually depends on which byte range of the stale object the bug still touches, so the replacement has to place an interesting field (a pointer to leak, a pointer to overwrite) at exactly the right offset.
- and the replacement must actually be reachable: there has to be a code path that allocates it, ideally on demand.

Hunting for structs that satisfy all three by hand is impractical at scale. This is where querying the binary as data pays off.

The previous hunt confirms a known bug in a known place. A different, harder question comes up during exploitation: given a use-after-free, which kernel objects can reclaim the freed slot and give us a useful primitive? BinQL can help on candidate shortlisting too.

CVE-2023-20938 is a use-after-free in Android’s binder driver that leaves a binder_node dangling in the kmalloc-128 slab. A viable replacement object is any struct that:

- lands in the same slab bucket (kmalloc-128, i.e. size in (96, 128]).
- has a pointer-width field (an 8-byte member, a pointer or any 64-bit value) at an offset the bug can reach.
- can be made to be allocated by the kernel from an unprivileged syscall.

Constraint 2 needs the specifics of this bug. When the dangling binder_node is reclaimed, the driver still operates on it through two code paths, each writing or reading a fixed window of the object:

- the unlink path touches bytes [0x20, 0x38) and lets the attacker corrupt whatever field the replacement object places there.
- the leak path reads bytes [0x58, 0x68) and discloses whatever the replacement object stored there.

So a useful replacement is one whose layout puts an 8-byte pointer squarely inside one of those two windows: a pointer in the unlink range gives a write primitive, a pointer in the leak range gives an infoleak. That is exactly what the query below encodes.

We deliberately picked a public documented case: the exploit is written up in detail, so we have a ground truth to check our results against. That the target kernel is open source is part of the point: the C/C++ CodeQL extractor could handle it too, so this is a fairer comparison than a case rigged in BinQL’s favour. We still run it through BinQL because the exact same query then runs unchanged on a closed-source kernel, where CodeQL has no source to ingest. That is where variant hunting like this really pays off.

We scan every struct in the extracted vmlinux database against those constraints:

```
// Constraint 1: same slab bucket as the freed binder_node (kmalloc-128).

predicate

isKmalloc128Sized
(
StructureType

st
) {

st
.
getSize
() >
96.0

and

st
.
getSize
() <=
128.0

}

predicate

isCandidateStruct
(
StructureType

st
,
Field

f
,
int

off
,
string

label
) {

// exclude the freed object itself

not

st
.
getName
() =
"binder_node"

and

f
 =
st
.
getAField
()
and

f
.
getDeclaratingType
() =
st

and

// Constraint 2: a pointer-width field (8-byte member or pointer type)...

  (
f
.
getType
().(
BasicType
).
getSize
().(
int
) =
8

or

f
.
getType
()
instanceof

PointerType
)
and

off
 =
f
.
getOffset
()
and

off
 %
8
 =
0

and

  (

// ...landing in the UNLINK window (bytes 32..56)...

    (
off
 <
56

and

off
 +
8
 >
32

and

label
 =
"UNLINK"
)
or

// ...or in the LEAK window (bytes 88..104).

    (
off
 <
104

and

off
 +
8
 >
88

and

label
 =
"LEAK"
)
  )
}
```

Constraint 3 is where analysing a binary differs from analysing source. To confirm it, we need to know that some allocation call actually produces our structure, and that a syscall can reach the function making that call.

The first half is the hard part. BinQL has no dataflow analysis yet, so it cannot follow a kmalloc’s return value and prove it becomes a struct X *. As a stand-in, we require the two facts to sit close together in the code: the allocation call and the type evidence for X (a (X *) cast, or a variable or parameter typed X *) must appear in the same function.

The second half, syscall reachability, could only be recovered from direct calls, as IDA has no runtime information about the binary.

This proximity heuristic is explicitly a workaround for a current BinQL limitation, not the only way to approach it, and once dataflow lands (see Future work) the same intent is expressed properly. More importantly, it is a reminder of how CodeQL is meant to be used: it narrows the search space. The heuristic will miss a some structures and it will flag a few that turn out not to be reachable. That is fine. Its job is to turn “every struct in the kernel” into a short list of plausible candidates. Deciding which of them actually yields a usable primitive, is the analyst’s role.

On a pre-fix Pixel 6 vmlinux (android13-5.10), the two queries return 20 structs:

structsizefield offsetreachable viaA`epitem`12840`ep_insert` ← epoll_ctlB`binder_ref`11288`binder_inc_ref_for_node` ← `BINDER_WRITE_READ`C`socket`12832`io_issue_sqe` ← io_uringD`file_system_type`10432`path_mount` ← mount()E`mnt_namespace`12832`create_new_namespaces` ← unshare/cloneF`bpf_reg_state`12096`do_check` ← bpf()&mldr;&mldr;&mldr;&mldr;&mldr;

Notably, the query rediscovers the two primitives the reference exploit relies on:

- B. giving an infoleak on the freed binder_node.
- A. cross-cached on top of the reclaimed slab.

The other eighteen are not noise to discard either: each is a struct that fits the bug as described in our CodeQL query, and several could plausibly drive an exploit. From a single dangling binder_node, BinQL lets you query the binary to review the shortlist manually.

# Conclusion

BinQL works today, but it is also a starting point: here is where it is headed, how it sits among similar efforts, and what we would like you to remember.

## Future work

BinQL is young, and several directions are open. Roughly in the order we intend to tackle them:

- We want to add data flow, because it is the feature that makes CodeQL more than structural matching, and the one the Enumerate UAF heap-spray candidates section had to work around with a proximity heuristic. The extractor would emit the facts and the binary library would expose them, porting to binaries what the C/C++ libraries already do on source.
- We want to support more decompilers, because the DBSCHEME was deliberately kept decompiler-agnostic, so Ghidra and Binary Ninja are the natural next targets and would free BinQL from IDA. Either the AST is read straight from their APIs, or their pseudocode is parsed with tree-sitter and a custom grammar, the same path the `codeql-solidity` project took to add Solidity to CodeQL.

## Gaining Traction for humans and LLM

BinQL is not the only project exploring this space of exposing binaries as structured data.

At REcon 2026, Elias Bachaalany (@eliasbchlny / @allthingsida) presented SELECT * FROM binary | Vibe Reversing Across IDA, Ghidra, and Binary Ninja, introducing xSQL, a cross-tool SQL interface over binary artefacts.

In January 2026, Binarly introduced VulHunt, a commercial platform for binary pattern matching at scale with their own engine, BIAS, built on Ghidra.

These projects each make a different design choice. xSQL and VulHunt build their own query stack, which gives them full control over the query model and the tooling around it. BinQL takes the opposite route: rather than writing an engine, it extends CodeQL, inheriting its query language, its existing libraries and its IDE integration, at the cost of having to fit the binary world into CodeQL’s data model.

## In the age of AI

Querying binaries as structured data is becoming a discipline of its own, and AI is about to accelerate it. The hard part of CodeQL has always been writing a good query, and LLMs are starting to do exactly that, synthesizing queries straight from a CVE or a plain-language bug description (QLCoder, CQLLM).

So far that only worked where source exists. BinQL removes that constraint: point the same automation at a binary and you get AI-assisted variant hunting on closed-source targets, from embedded firmware to proprietary desktop applications.

## Last words

Three things to take away:

- A CodeQL extractor is not a black box. We reverse-engineered its undocumented formats, understood the pipeline end to end, and built our own, so you can extend CodeQL to targets it was never meant to reach.
- One query language, source or not. BinQL gives you the same CodeQL interface whether you hold the source code or just the stripped binary.
- We put it to work on real targets. It can be used for hunting variants, tracking a vulnerable library across shipped versions, and shortlisting objects for an exploit.

You can find the latest BinQL version on our GitHub, along with installation instructions.

If you are a daily CodeQL and/or IDA user, we invite you to give it a try. Ideas for improvement and bug reports are welcome.

- The two lowering phases (QL → DIL → RA) are detailed in “CodeQL: Also a Powerful Binary Analysis Engine”, BlackHat USA 2023. ↩︎
- CodeQL GitHub repository issues on building and creating an extractor. ↩︎
- CodeQL GitHub repository discussion on generating HTML documentation for a custom CodeQL library ↩︎
- Inspired by CodeQL’s homepage: “CodeQL lets you query code as though it were data.” ↩︎
