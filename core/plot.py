import plotly.graph_objects as go

class plot:
    """
    This class will be used to create all necessary plots in a consistent format.
    """

    def __init__(self, fig=None, width=800, height=400, title_size=14, tick_size=10, axis_size=10, font_size=10, show_fig=False) -> None:
        if not fig:
            self.fig = go.Figure()
        else:
            self.fig = fig
        self.width = width
        self.height = height
        self.title_size = title_size
        self.tick_size = tick_size
        self.axis_size = axis_size
        self.font_size = font_size
        self.show_fig = show_fig
        self.margin = {
            't': 100,
            'b': 100,
            'l': 100,
            'r': 100
        }
        self.font_family = 'Arial'
        self.colorDict = {
                'primary': '#1C4C38', 
                'secondary': '#005288',
                'first_grey': '#C4C4C4', 
                'light_grey': '#f9f9f9'
        }
        self.colorList = [
                '#005288', 
                '#1C4C38',
                '#01B2B3', 
                '#DD663C', 
                '#A899A5', 
                '#492a42', 
                '#d8eded', 
                '#bdd7e5', 
                '#bdd7e5'
            ]
        self.show_legend = True

    def _set_layout(self, x_label=None, y_label=None, title=None, legend_title=None) -> None:
        """
        A function to format the plot into the chosen layout
        It should be run after each plotting function.
        """

        layout = go.Layout(
            height=self.height,
            width=self.width,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(
                font=dict(
                    color='#000000',
                    size=self.title_size
                ),
                text=title
            ),
            #margin=self.margin,
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend_title=legend_title,
            showlegend=self.show_legend,
            colorway=self.colorList
        )

        self.fig.update_layout(layout)
        self.fig.update_xaxes(linewidth = 1, linecolor ='black', tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size))
        self.fig.update_yaxes(
            linewidth = 1, 
            linecolor = 'black', 
            tickfont=dict(family=self.font_family, color='#000000', size=self.tick_size),
            #tick0=200,
            dtick=200
        )

    def _set_end_label(self, x, y, text, color):
        """
        This function should be used to create labels at the right side of the graph

        Args:
            x (float): The most right variable on the x axis
            y (float): The height of the label
            text (str): The label text
            color (str): The hex color of the text (same as line)
        """

        # Making room for the labels
        self.margin['r'] *= 1.15
        self.fig.add_annotation(
            x=1.05,
            y=y,
            xref="paper",
            yref="y",
            text=text,
            font=dict(
                family=self.font_family,
                size=self.font_size,
                color=color
                ),
            align="left",
            ax=0,ay=0
        )
        self.show_legend=False

    def create_text_box(self, distance:int, meters_up:int, meters_down:int, duration):
        text = f'''
            Distance: {distance:,.0f}m <br>
            Højdemeter op: {meters_up:,.0f} <br>
            Højdemeter ned: {meters_down:,.0f} <br>
        '''
        self.fig.add_annotation(
            x=0.9,
            y=0.9,
            xref="paper",
            yref="paper",
            text=text,
            font=dict(
                family=self.font_family,
                size=self.font_size,
                color='black'
                ),
            align="right",
            ax=0,ay=0,
            #bordercolor="#f9f9f9",
            #borderwidth=2,
            #bgcolor="#f9f9f9",
            #opacity=0.85,
        )

    def continuous_grouped(
        self, 
        x, 
        y, 
        group, 
        mode='lines', 
        colors=None, 
        x_title: str=None,
        y_title: str=None, 
        title: str=None, 
        end_annotation: bool=False, 
        show_textbox:bool=False
        ):
        """Building a plot with multiple line plots

        Args:
            x (list): List of x values
            y (list): List of y values
            group (list): List of grouping
            mode (str, optional): The scatter plot type. Defaults to 'lines'.
            colors (list, optional): List of colors for the groups. Defaults to None.
            x_title (str, optional): X title. Defaults to None.
            y_title (str, optional): Y title. Defaults to None.
            title (str, optional): Plot title. Defaults to None.
            end_annotation (bool, optional): If there should be an end annotation to the lines. Defaults to False.
            show_textbox (bool, optional): If there should be a text box in the top right corner of the graph with describtives

        Returns:
            go.Figure: The figure just created.
        """
        groups = list(dict.fromkeys(group))   
        group_indexex = [{group_value: [i for i, x in enumerate(group) if x==group_value]} for group_value in groups] 
        if colors is None:
            colors = [None] * len(groups)

        for group_value, color in zip(group_indexex, colors):
            for group_name, index in group_value.items():
                x_list = [x[i] for i in index]
                y_list = [y[i] for i in index]

                self.fig.add_trace(
                    go.Scatter(
                        x=x_list, y=y_list,
                        mode=mode,
                        name=group_name,
                        marker=dict(color=color),

                        # Creating pretty hover boxes
                        customdata=[group_name]*len(y_list),
                        hovertemplate = "%{customdata}: %{y}<extra></extra>"
                    )
                )
            
                if end_annotation:
                    self._set_end_label(x=x_list[-1], y=y_list[-1], text=group_name, color=color)

        self._set_layout(x_label=x_title, y_label=y_title, title=title)
        if self.show_fig:
            self.fig.show()

        return self.fig
    

    def continuous(self, x, y, name=None, mode='lines', x_title=None, y_title=None, title=None, end_annotation=False):
        self.fig.add_trace(
            go.Scatter(
                x=x, y=y,
                mode=mode,
                name=name,
                marker=dict(color=self.colorDict.get('primary')),

                # Creating pretty hover boxes
                hovertemplate = "%{y}<extra></extra>"
            )
        )
        self._set_layout(x_label=x_title, y_label=y_title, title=title)
        
        if end_annotation:
            self._set_end_label(x=x[-1], y=y[-1], text=name, color=self.colorDict.get('primary'))

        self._set_layout(x_label=x_title, y_label=y_title, title=title)
        if self.show_fig:
            self.fig.show()

        return self.fig

    def show(self):
        self.fig.show()

def main():
    x = [1,2,3,1,2,3]
    y = [1,2,2,2,3,5]
    group = ['a', 'a', 'a', 'b', 'b', 'b']

    a=plot(show_fig=False)
    a.create_text_box(distance=2,meters_up=2,meters_down=2,duration=2)
    a.continuous_grouped(x, y, group, end_annotation=True, show_textbox=True)
    a.fig.show()
    #plot(show_fig=True).continuous(x[:3], y[:3], end_annotation=True)

if __name__=='__main__':
    main()