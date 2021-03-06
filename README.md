# rouse-a-greek-boy-at-home

A repo of Rouse's *A Greek Boy at Home* based on the epub generated by [Dave Maddock](https://github.com/dmaddock1) from [Archive.org's copy](https://archive.org/details/greekboyathomest01rousuoft) and manually checked against it by  Dave and Fletcher.

Comments and corrections welcome!

This work is licensed under a [CC BY SA licence](https://creativecommons.org/licenses/by-sa/4.0/).



# Note on repo structure

There are four directories for files depending on their status:

* `todo` files that noone has started proofing
* `drafts` files that are currently being proofed by someone. Feel free to create your own sub directory if you like.
* `src` files that are done
* `docs` html formatted file for viewing on project github pages site.

# Scripts
There several scripts to help with the processing of the files. They're all located in `drafts/scripts/`.
* `add_line_numbers.py <FILE_NAME>` - takes file (from draft folder), reformats it to the defined line format and saves it to the `src/<FILE_NAME>` folder.
* `build_static.py` - takes the `md` files from `src` folder and generates proper `HTML` files in the `docs` folder.
* `run-checks.py <opt: FILE_NAME_1, FILE_NAME_2,...>` - check the files provided as args or hardcoded in the script for proper encoding
* `split-to-chapters.py` - ???

# Progress

**19/43**

| File | Proofed | Being checked by |
|:--- |:--- |:---|
| greek-boy-ch02.md | Y |  |
| greek-boy-ch04.md | Y |  |
| greek-boy-ch06.md | Y |  |
| greek-boy-ch07.md | Y |  |
| greek-boy-ch08.md | Y |  |
| greek-boy-ch09.md | Y |  |
| greek-boy-ch10.md | Y |  |
| greek-boy-ch11.md | Y |  |
| greek-boy-ch12.md | Y |  |
| greek-boy-ch13.md | Y |  |
| greek-boy-ch14.md | Y |  |
| greek-boy-ch15.md | Y | Chris |
| greek-boy-ch16-17.md | N | Fletcher |
| greek-boy-ch18.md | Y | Chris |
| greek-boy-ch19.md | N | Chris |
| greek-boy-ch20.md | N |  |
| greek-boy-ch21.md | Y | Chris |
| greek-boy-ch22.md | Y | Chris |
| greek-boy-ch23.md | Y | Chris |
| greek-boy-ch24.md | N |  |
| greek-boy-ch25.md | Y | Chris |
| greek-boy-ch26.md | Y | Chris |
| greek-boy-ch27.md | Y | Chris |
| greek-boy-ch28.md | N |  |
| greek-boy-ch29.md | N |  |
| greek-boy-ch30.md | N |  |
| greek-boy-ch31.md | N |  |
| greek-boy-ch32.md | N |  |
| greek-boy-ch33.md | N |  |
| greek-boy-ch34.md | N |  |
| greek-boy-ch35.md | N |  |
| greek-boy-ch36.md | N |  |
| greek-boy-ch37.md | N |  |
| greek-boy-ch38.md | N |  |
| greek-boy-ch39.md | N |  |
| greek-boy-ch40.md | N |  |
| greek-boy-ch41.md | N |  |
| greek-boy-ch42.md | N |  |
| greek-boy-ch43.md | N |  |
| greek-boy-ch44.md | N |  |
| greek-boy-ch45.md | N |  |

# Note on file format

The file format for the data files is based on a common format being used by the [greek-texts project](https://jtauber.github.io/greek-texts/).

Each line of a file begins with an text part address in the form of `Chapter-number.Line-number` then a space and the content which is marked up with Markdown. For example, the following snipped is a Heading 1 from chapter three, line one. Each line corresponds roughly to a paragraph unless it has some kind of marking to specify otherwise.

```
3.1 # III ΚΗΠΟΣ
```

This project also needed line numbers which appear in the text with the following format `{page-number.line-number}`. The page number corresponds to the page number in the PDF file. Thus in the following example which is the first line of the fourth chapter, the line corresponds to lines 16, 17, and 18 found on page 11 of the PDF file.

```
4.1 {11.16} ὥρα νῦν λέγειν σοι τὰ περὶ τῆς οἰκίας. μικρὰ {11.17} μέν ἐστιν ἡ οἰκία ἡμῶν, μικροτάτη μὲν οὖν· τί μήν; {11.18} οὐ γὰρ πολλοί ἐσμεν, οὐδὲ πλούσιοι.
```

Finally, this project needed footnotes which have the following format. The foot content is marked by giving it the same Chapter and Line number as the line it relates with the addition of `.fn` and a number to the text part address. The location of the footnote in its line is marked by an inline anchor formed by adding the `.fn` and number in square brackets. In the following example line `3.10.fn1.add` is the footnote content which corresponds to the part of line `3.10` marked by the anchor `[fn1.add]`. The particular pieces added after the Chapter and Line number don't matter too much as long as they are consistent and match the inline footnote anchor.

```
3.10 ... τὸ δ’ αὐτὸ ποιοῦμεν καὶ ἡμᾶς [fn1.add]· οὐδὲ θαυμάζει ....
3.10.fn1.add > ἡμεῖς
```
