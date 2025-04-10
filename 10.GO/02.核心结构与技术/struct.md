
Go 语言中的 `struct`（结构体）是非常核心的概念之一，它用来定义一组**字段的集合**，可以理解为“定制版的数据类型”，类似于其他语言中的 **class**（不过没有继承哦）。

---

## 🔧 基本用法

### 1. 定义结构体

```go
type Person struct {
    Name string
    Age  int
}
```

上面定义了一个名为 `Person` 的结构体，它有两个字段：`Name`（字符串）和 `Age`（整数）。

---

### 2. 创建结构体变量

```go
// 方法一：声明 + 赋值
var p1 Person
p1.Name = "Alice"
p1.Age = 30

// 方法二：字面量初始化（推荐）
p2 := Person{"Bob", 25}

// 方法三：带字段名初始化（更清晰）
p3 := Person{Name: "Charlie", Age: 40}
```

---

### 3. 访问和修改字段

```go
fmt.Println(p3.Name) // 输出: Charlie
p3.Age = 41          // 修改字段
```

---

### 4. 指针结构体（非常常见）

```go
p := &Person{Name: "Dora", Age: 28}
p.Age++  // Go 会自动解引用，等同于 (*p).Age++
```

---

### 5. 嵌套结构体

结构体可以嵌套其他结构体，非常适合构建层级数据：

```go
type Address struct {
    City  string
    Zip   string
}

type Employee struct {
    Name    string
    Address // 匿名字段（嵌入）
}
```

你可以这样访问嵌套字段：

```go
emp := Employee{Name: "Eve", Address: Address{City: "Shanghai", Zip: "200000"}}
fmt.Println(emp.City)  // 输出: Shanghai
```

---

### 6. 匿名字段（也叫“内嵌字段”）

```go
type Human struct {
    Name string
}

type Student struct {
    Human  // 匿名字段，自动“继承”字段
    School string
}
```

这样 `Student` 可以像继承一样访问 `Human` 的字段：

```go
stu := Student{Human: Human{Name: "Frank"}, School: "Go大学"}
fmt.Println(stu.Name)  // 输出: Frank
```

---

## 🧠 struct 小贴士

| 用法        | 说明 |
|-------------|------|
| `type StructName struct {}` | 定义结构体类型 |
| `var s StructName`          | 创建结构体变量 |
| `&StructName{}`             | 创建结构体指针 |
| 匿名字段嵌入                 | 可实现类似继承的效果 |
| 结构体是值类型              | 赋值会复制整个结构体（除非用指针） |

---

如果你想要进一步玩转 `struct`，可以试试结合 `json` 标签、接口（`interface`）使用