import pandas as pd
import plotly.express as px


def plan_vs_actual_fig(budget, actual):
  actual_sum_by_category = actual.groupby('category')['amount'].sum()
  actual_sum_by_category = pd.DataFrame(
      actual_sum_by_category.rename('amounts'))
  actual_sum_by_category['source'] = 'actual'
  budget['source'] = 'budget'
  df = pd.concat([budget.set_index('items'), actual_sum_by_category])
  return px.bar(df, x=df.index, y='amounts', color='source', barmode="overlay")


def piechart(names, values):
  return px.pie(names=names, values=values, hole=.9)


def plan_vs_actual_time_series(budget, actual):
  actual = actual.set_index('date')
  return px.line(
      x=actual.index, y=actual['amount'].cumsum() / budget['amounts'].sum())
