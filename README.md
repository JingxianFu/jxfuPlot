This is a tutorial that can teach you how to use this program.
---
# jxfuPlot
It's a small python package to help you drawing a barplot with error bar and significance (*).

# Introduction
  We can not find a python package that help you to draw a bar plot with error bar and significance, but these two elements are important in our statistic analysis when dealing with a big data in biological or economic project. To draw a plot with error bar and * conveniently, I designed a package based on seaborn, matplotlib, scipy and others.

# Tutorials
## Install requirements
  Firstly, you should make sure your evironment is required for `requirements.txt`. If you don't know whether you have the evironment, you can try this code in Terminal or CMD.
  ```
  pip install -r requirements.txt
  ```
  It can help you to install necessary package for my program.
## Drawing your first plot!
  You should open draw_significance.py and run it directly, and then the plot will show for you.
  ![image](https://user-images.githubusercontent.com/65908422/221524862-5c06c078-c028-4b30-aa51-50a84620a3e5.png)

  Or you can create your `.py` file, and the try:
  ```python
  from draw_significance import plot_sig_bar
  # df is Dataframe from pd.Dataframe''
  plot_sig_bar(df)
  ```
  Make sure your first column and second column are, respectively, tag(str) and value(float) in df, just like the format in `test_1.csv`

# End of all
  it is my first upload, and this program is not perfect, but I will try and try to learn more and create more
