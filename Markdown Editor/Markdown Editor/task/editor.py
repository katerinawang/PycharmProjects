def text(f, md=""):
    if f not in ["header", "link", "new-line", "ordered-list", "unordered-list"]:
        ipt = input("Text:")
        if f == "bold":
            md = f"**{ipt}**"
        if f == "italic":
            md = f"*{ipt}*"
        if f == "inline-code":
            md = f"`{ipt}`"
        if f == "plain":
            md = ipt
    if f == "new-line":
        md = f"\n"
    if f == "header":
        lv = int(input("Level:"))
        while lv not in range(1, 7):
            print("The level should be within the range of 1 to 6")
            lv = int(input("Level:"))
        txt = input("Text:")
        md = "#"*lv + " " + txt + "\n"
    if f == "link":
        lb = input("Label:")
        url = input("URL:")
        md = f"[{lb}]({url})"
    if f in ["ordered-list", "unordered-list"]:
        rows = int(input("Number of rows:"))
        lst = []
        while rows <= 0:
            print("The number of rows should be greater than zero")
            rows = int(input("Number of rows:"))
        for i in range(rows):
            i += 1
            lst.append(input(f"Row #{i}:"))
        if f == "ordered-list":
            nums = []
            for i in range(len(lst)):
                i += 1
                nums.append(str(i))
            md = "".join(map(lambda x, y: x + ". " + y + "\n", nums, lst))
        if f == "unordered-list":
            md = "".join(map(lambda x: f"* {x}\n", lst))
    return md


class MarkdownEditor:

    form = ["plain", "bold", "italic", "header", "link", "inline-code", "ordered-list", "unordered-list", "new-line", "!help", "!done"]

    help = "Available formatters: "+" ".join(form[:-2]) + "\nSpecial commands: !help !done"

    def formatter(self, lst=""):
        fmt = input("Choose a formatter:")
        if fmt not in [k for k in self.form]:
            print("Unknown formatting type or command")
            return self.formatter(lst)
        if fmt == "!help":
            print(self.help)
        if fmt == "!done":
            with open("output.md", "w") as f:
                f.write(lst)
            return
        lst += text(fmt)
        print(lst)
        return self.formatter(lst)


mark = MarkdownEditor()
mark.formatter()
