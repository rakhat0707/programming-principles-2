# TSIS1 — How to Use (Short Demo Guide)

## 🚀 Запуск

```bash
cd TSIS/TSIS1
python phonebook.py
```

---

## 🧪 Демонстрация

### 1. Add contact

```
1
Name: Aida
Email: aida@gmail.com
Birthday: 2005-05-05
Group: Friends
```

---

### 2. Add phone

```
2
Contact name: Aida
Phone: 87005556677
Type: mobile
```

---

### 3. Move group

```
3
Name: Aida
New group: Work
```

---

### 4. Search

```
4
gmail
```

---

### 5. Filter by group

```
5
Work
```

---

### 6. Sort

```
6
name
```

или

```
birthday
```

---

### 7. Pagination

```
7
next
prev
quit
```

---

### 8. Export JSON

```
8
```

→ создаётся `contacts.json`

---

### 9. Import JSON

```
9
```

→ загружает данные в БД

---

### 10. Import CSV

```
10
```

→ читает `contacts.csv`

---

## 🧪 Проверка SQL

```sql
SELECT * FROM contacts;
SELECT * FROM phones;
SELECT * FROM groups;
```

---

## ✅ Итог

* добавление контактов
* несколько телефонов
* группы
* поиск
* фильтр
* сортировка
* pagination
* JSON и CSV импорт/экспорт
