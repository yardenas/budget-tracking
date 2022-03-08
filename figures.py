import plotly.express as px
from dash import dcc


def plan_vs_actual_fig(budget):
  return dcc.Graph(
      id='plan_vs_actual_all_budgetary_items',
      figure=px.bar(budget, x='items', y='amounts'),
      className='figure')


def piechart(names, values):
  return dcc.Graph(
      id='piechart',
      figure=px.pie(names=names, values=values),
      className='figure')
