import pandas as pd
import plotly.express as px


def plan_vs_actual_fig(budget, actual):
  actual_sum_by_category = actual.groupby('category')['amount'].sum()
  actual_sum_by_category = pd.DataFrame(
      actual_sum_by_category.rename('amounts'))
  actual_sum_by_category['source'] = 'actual'
  budget['source'] = 'budget'
  df = pd.concat([budget.set_index('items'), actual_sum_by_category])
  return px.bar(
      df,
      x=df.index,
      y='amounts',
      color='source',
      barmode="overlay",
      color_discrete_map={
          "budget": "DeepSkyBlue",
          "actual": "#1260CC",
      },
      template="simple_white")


def piechart(names, values):
  return px.pie(
      names=names,
      values=values,
      hole=.9,
      color=names,
      color_discrete_map={
          name: color for name, color in zip(names, [
              '#b7f0ff', '#7ae4ff', '#7ae9ff', '#3dd5ff', '#3dd8ff', '#00a3cc',
              '#007a99', '#008099', '#005366', '#004f66', '#002833'
          ])
      })


def plan_vs_actual_time_series(budget, actual):
  actual = actual.set_index('date')
  return px.line(
      x=actual.index, y=actual['amount'].cumsum() / budget['amounts'].sum())
