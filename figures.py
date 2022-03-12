import plotly.express as px
from dash import dcc


def plan_vs_actual_fig(budget, actual):
  return px.bar(budget, x='items', y='amounts')


def piechart(names, values):
  return px.pie(names=names, values=values, hole=.9)


def plan_vs_actual_time_series(budget, actual):
  actual = actual.set_index('date')
  return px.line(
      x=actual.index, y=actual['amount'].cumsum() / budget['amounts'].sum())
