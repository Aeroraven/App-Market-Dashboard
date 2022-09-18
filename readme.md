<h2 align = "center"> Assignment 3 for Human Computer Interaction</h2>
<h3 align = "center">Data Visualization</h3>
<p align="center">Aeroraven</p>



### 0. How to Run 

#### 0.1 Prerequisite Packages

The dependencies should be installed via `pip` or `conda`

- dash
- plotly
- numpy
- pandas
- wordcloud
- **dash-dangerously-set-inner-html**
- **dash-bootstrap-components**

#### 0.2 How to Start

Then run app.py

```shell
python app.py
```

Then, open the browser and visit `http://localhost:8050`





### 1. Description of the Dataset & Goal

#### 1.1 Dataset Overview

The dataset adopted in this lab is Google Play Store Dataset, which contains recent statistical data of popular mobile application available on Google Play Store, together with some comments from several applications(a subset of the main table)

The dataset describes application in different indicators, including user ratings, prices, reviews, installs, sizes and sentiment polarities of comments. Also, descriptive information like categories, genres, content ratings, versions are attached to each element in the data to make the information complete.

Here are the details of each indicator

- **Category & Genre**: Describes the genre of the application. For example, the category for app `Discord ` is 'communication', and the category for app `LinkedIn` is 'social'
- **Rating**: Describes the user-voted quality of the application. The maximum is 5, which means the application enjoys a high reputation among users, and the minimal value is 1 because of the system mechanism.
- **Reviews**: Describes the number of reviews by users
- **Size**: Describes the size of the application. Namely, the storage space occupied by the application
- **Installs**: The dataset only provides the approximate lower bound of the exact installs.  For example, '5000+' means the number of installs in ranged between 5000 and 10000.
-  **Type & Price**: Indicates whether the app is free-to-use or not
- **Content Rating**: A content rating rates the suitability of TV broadcasts, movies, comic books, or video games to its audience. The dataset adopts ESRB criterion.
- **Last Update & Current Version**: Information about the latest update of the application
- **Android Ver**: This describes the required platform, architecture or version of the client smartphone.

And for the sentiment dataset, columns involves:

- **Translated Sentences**: Contains translated comments in english
- **Sentiment**: Indicates the sentiment of the comment is whether positive, neutral or negative.
- **Sentiment Tendency**: The AI-evaluated tendency of the comment sentiments.

#### 1.2 Goal Description

Data visualization is primarily designed to communicate and communicate information clearly and effectively through graphical means. The task of data visualization involves: 

| ***Task Categories***         | ***Task Types***                                             |
| ----------------------------- | ------------------------------------------------------------ |
| *Data and view specification* | **Visualize** data by choosing visual encodings; **Filter** out data to focus on relevant items; **Sort** items to expose patterns; **Derive** values of models from source data |
| *View manipulation*           | **Select** items to highlight, filter, or manipulate; **Navigate** to examine high-level patterns and low level detail; **Coordinate** views for linked exploration; **Organize** multiple windows and workspaces |
| *Process and provenance*      | **Record** analysis histories for revisitation, review, and sharing; **Annotate** patterns to document findings; **Share** views and annotations to enable collaboration; **Guide** users through analysis tasks or stories |

The design goal for the dashboard(Google Play Dataset Dashboard) includes:

- **Interaction Design**: Design a user-friendly interface
  - **Keeping Interaction**: Some interactive controls (like combo boxes) are necessary for users to perform necessary data manipulation operations (like filtering & search).
  - **Keeping Simplicity**: Too complex interaction is not user-friendly. Thus we need to avoid redundant interactive components which rebel against the principle of  dashboard design. This means, too many buttons, check boxes should be avoided.
  - **Avoiding Improper Pursuit of Aesthetics**: For example, avoiding too many colors and decorations, which might make users distracted.

- **Functional Design**: 
  - **Data Representation**: Represent the data in proper forms. For example, a histogram to show the rating distribution for a certain app category. And the graphs should visualize core information instead of useless information.
  - **Data Comparison**: Users can compare data in different temporal, categorical or spatial conditions. For example, the comparision between the information of app `Snapseed` and the average indicators of all photography apps.
  - **Data Subdivision**: Visualize the data in different levels (or in a hierarchy). 

And the analytical task might include:

- **Categorical Information Analysis**: Provide key information about certain categories (Eg. Category `Shopping`). Or the information to do with comparison between categories.
- **Application Information Analysis**: Provide key information about a certain app (Eg. `Facebook` or `Youtube`). Information related to comparison between apps is also eligible.

#### 1.3 Overall Framework

The dashboard for lab3 is implemented via `Dash` framework. Data manipulation is done via `Pandas` library, together with `Wordcloud` library and `Numpy` library.

#### 1.4 Overall Functions

- **Interaction**: Users can select target categories or apps
- **Representation**: 7 different graphs are used to visualize the dataset. Details will be described in section 2.

### 2. Description of Details

#### 2.1 Overall Layout

The overall layout adopted is double-column layout. The left part of the dashboard mainly focuses on categorical data (like rating for a overall category), and the right part focuses on a single app (eg. `Twitter`). 

The overall layout is shown in the following snapshot. (Example: Game, Honkai Impact 3rd)

![image-20220624204538196](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624204538196.png)

#### 2.2 Graph 1: Categorical Popularity & Quality Map

In this assignment, I used the scatter plot to visualize the distribution of popularity and quality of a certain categories. The plot also depicts the relation between popularity and the quality.

The indicator 'quality' is quantified by user ratings and the indicator 'popularity' is quantified by installs. The radius of circle is another quantification of 'popularity'.

Points on the right-top corner means the corresponding apps enjoy both high popularity and high reputation. And points located on left-top corner means  the corresponding apps might have high quality but lack popularity.

Here is an example graph (Example Category: House and Home)

![image-20220624205416657](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624205416657.png)

Users can also use the mouse to move over points to check its corresponding name. This can help users discover new apps.

#### 2.3 Graph 2: Category Indicator

To depict the characteristics of a given category, I defined five dimensions, including Rating, Price, Popularity, Review and Variety.

- **Rating**: The arithmetic average of user ratings of all apps that belong to this category.
- **Review**: The arithmetic average of user reviews of all apps that belong to this category.
- **Popularity**: The arithmetic average of user installs of all apps that belong to this category.
- **Variety**: Numbers of app that belongs to this category
- **Price**: The arithmetic average price of all apps that belong to this category.

But simply illustrating the indicators using bar graph or pie graph is far from abundant. The trait of a given category can be stressed by comparison with other categories. Thus, a radar graph is adopted to visualize these indicators.

Here is an example graph (Example Category: Tools)

![image-20220624210514806](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624210514806.png)

Using the radar graph, we can easily find that utility apps are more diversified,. We can also find that the tool-app users are tend to post their reivews online. The comparision forms the unique characteristics for tool apps

#### 2.4 Graph 3: Content Rating Distribution

This pie chart illustrates the distribution of content rating for a certain category. From this chart, we can find who these apps are developed for.

Here is an example graph (Example Category: Game)

![image-20220624211019119](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624211019119.png)

The pie chart above shows that almost half of games are intended for everyone. However, the remaining parts are intended for teens or older people.

#### 2.5 Graph 4: Categorical Rating Distribution

This histogram shows the distribution of ratings of a certain genre. Although rating has already been modeled and visualized in graph 1, this graph provided a more straightforward illustration of the apps of a certain category.

Normally, the shape of the histogram is a Gaussian curve(with means $\mu$ and variance $\sigma^2$). If the curve is fat (or with large $\sigma$), we will say the apps in this category is uneven (some good and some bad). If the maximizer of the curve is small (or with small $\mu$), we will say the the apps in this category is far from user's expectation. Thus, histogram is more straightforward than the scatter plot.

Here is an example graph (Example Category: Travel and Local)

![image-20220624211421961](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624211421961.png)

#### 2.6 Graph 5: App Indicators

After selecting a parent genre, users can select a app using the dropdown component. Here are three traditional gauges that illustrate main attributes of a given app.

- **Rating**: The rating of a app. The red line is the average score of all apps that belong to this category.
- **Topicality**: The reviews of a app. The red line is the average score of all apps that belong to this category.(Logarithmic metric is used to avoid unbalanced range)
- **Popularity**: The total installs of a app. The red line is the average score of all apps that belong to this category. (Logarithmic metric is used to avoid unbalanced range)

This gauge reflects whether an app is high-quality or high-popularity, using the comparison with the average value.

Here is an example graph (Example App: Angry Birds 2)

![image-20220624212747449](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624212747449.png)

We can see that the game Angry Birds 2 enjoys all quality, topicality and popularity.

#### 2.7 Graph 6: Comment Word Cloud

A word cloud is a visual representation of text data, which is often used to depict keyword metadata on websites, or to visualize free form text. Tags are usually single words, and the importance of each tag is shown with font size or color.

Here, word cloud graph is used to extract the keypoints of comments for a given app. Users can easily find the key words and common comments about the app via comment word cloud.

Here is an example graph (Example App: Google)

![image-20220624214310897](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624214310897.png)

#### 2.8 Graph 7: Comment Sentiment Polarity

This bar chart depicts the comment sentiment tendency of a given app. There are only three bars, indicating positive comments, neutral comments and negative comments, so it's simple and obvious for dashboard users.

Here is an example graph (Example App: Google)

![image-20220624214905675](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624214905675.png)

#### 2.9 Miscellaneous Details

**Data cleaning**: Data provided is not suitable for data visualization because of the "dirty data". The cleaning step is done via both `Excel` and `Python Pandas`.

Example of "Dirty data":

![image-20220624220247782](C:\Users\huang\AppData\Roaming\Typora\typora-user-images\image-20220624220247782.png)

Here's an example to filter out `NaN` values and preprocess the raw data

```Python
for i in range(len(series_in)):
    if pd.isna(series_in[i]) or pd.isna(series_rt[i]) or pd.isna(series_rv[i]) or pd.isna(series_ap[i]):
        continue
        installs.append(2 + (math.log2(int(series_in[i].replace(",", "").replace("+", "")))))
        ratings.append(series_rt[i])
        reviews.append(series_rv[i])
        apps.append(series_ap[i])
```

**Handling User's Interaction**: This is done via `app.callback` annotation.

Here's an example.

```Python
@app.callback(
    Output('example-graph', 'figure'),
    Input("dropdown-category", 'value')
)
def acb_update_rating_dist(category):
    df_ratings = get_rating_stats(get_category_i(category))
    fig = px.histogram(df_ratings, x="Rating", nbins=40)
    fig.update_layout(title="Rating Distribution (Category)", template=pio.templates['plotly_dark'])
    fig.update_layout(template=pio.templates['plotly_dark'])
    return fig

```

**Subploting**: This is a feature implemented by many graph libraries, including plotly and matplotlib. This makes layout more dense.

Here's an example in the program.

```Python
@app.callback(
    Output('example-graph-8', 'figure'),
    Input("dropdown-app", 'value')
)
def acb_update_app(app_name):
    df_app_rating_id = get_app_rating_ref(app_name)
    df_app_reviews_id = get_app_reviews_ref(app_name)
    df_app_install_id = get_app_downloads_ref(app_name)
    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=df_app_rating_id,
        delta={'reference': df_radar_ct[1], 'increasing': {'color': "orange"}},
        title={'text': "Rating Indicator", 'font': {'size': 16}},
        gauge={'axis': {'range': [None, 5]},
               'bar': {'color': "orange"},
               'steps': [
                   {'range': [0, 1], 'color': "#444444"},
                   {'range': [1, 2], 'color': "#555555"},
                   {'range': [2, 3], 'color': "#666666"},
                   {'range': [3, 4], 'color': "#777777"},
                   {'range': [4, 5], 'color': "#888888"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': df_radar_ct[1]}},
        domain={'row': 0, 'column': 0})
    )
    fig_gauge.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=math.log10(int(df_app_install_id)),
        delta={'reference': math.log10(DataCache.avg_download), 'increasing': {'color': "orange"}},
        title={'text': "Popularity(Download) Indicator", 'font': {'size': 16}},
        gauge={'axis': {'range': [None, 8]},
               'bar': {'color': "orange"},
               'steps': [
                   {'range': [0, 1], 'color': "#444444"},
                   {'range': [1, 2], 'color': "#555555"},
                   {'range': [2, 3], 'color': "#666666"},
                   {'range': [3, 4], 'color': "#777777"},
                   {'range': [4, 5], 'color': "#888888"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75,
                             'value': math.log10(DataCache.avg_download)}},
        domain={'row': 1, 'column': 0})
    )
    fig_gauge.update_layout(template=pio.templates['plotly_dark'])
    fig_gauge.update_layout(grid={'rows': 2, 'columns': 1, 'pattern': "independent"})
    return fig_gauge
```





