import pandas as pd
import numpy as np
import plotly.express as px


def plan_vs_actual_fig(budget, actual):
  actual_sum_by_category = actual.groupby('category')['amount'].sum()
  actual_sum_by_category = pd.DataFrame(
      actual_sum_by_category.rename('amounts'))
  actual_sum_by_category['source'] = 'Actual spendings'
  budget['source'] = 'Budget'
  df = pd.concat([budget.set_index('items'), actual_sum_by_category])
  df['amounts'] = np.abs(df['amounts'])
  fig = px.bar(
      df,
      x=df.index,
      y='amounts',
      color='source',
      barmode="overlay",
      color_discrete_map={
          "Budget": "DeepSkyBlue",
          "Actual spendings": "#1260CC",
      },
      template="simple_white",
      height=450,
      width=425)
  fig.update_layout(xaxis_title="", yaxis_title="")
  fig.update_xaxes(tickangle=45)
  fig.update_layout(
      legend=dict(
          yanchor='top', y=-0.3, xanchor='left', x=0.01, orientation='h'),
      legend_title_text='')
  return fig


def piechart(names, values):
  fig = px.pie(
      names=names,
      values=np.abs(values),
      hole=.9,
      color=names,
      color_discrete_map={
          name: color for name, color in zip(names, [
              '#b7f0ff', '#7ae4ff', '#7ae9ff', '#3dd5ff', '#3dd8ff', '#00a3cc',
              '#007a99', '#008099', '#005366', '#004f66', '#002833'
          ])
      },
      height=450,
      width=425)
  fig.update_layout(
      legend=dict(
          yanchor='top', y=-0.3, xanchor='left', x=0.01, orientation='h'))
  return fig


def plan_vs_actual_time_series(budget, actual):
  actual = actual.set_index('date')
  actual.sort_index(inplace=True)
  # Aggregate and sum all items with the same date.
  actual_amounts_by_date = actual['amount'].groupby(
      actual['amount'].index).sum()
  fig = px.line(
      x=actual_amounts_by_date.index,
      y=actual_amounts_by_date.cumsum(),
      markers=True,
      template="simple_white",
      color_discrete_sequence=['DeepSkyBlue', '#004f66'],
      height=450,
      width=425)
  fig.update_traces(line=dict(width=2.5))
  fig.add_hline(
      y=budget['amounts'].sum(),
      opacity=1,
      line_width=2.5,
      line_dash='dash',
      line_color='black',
      annotation_text='Budget')
  fig.update_layout(xaxis_title="Date", yaxis_title="Money Spent")
  return fig
