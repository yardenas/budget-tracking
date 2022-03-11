import plotly.express as px
from dash import dcc, html


def plan_vs_actual_fig(budget):
  return dcc.Graph(
      id='plan-vs-actual-all-budgetary-items',
      figure=px.bar(budget, x='items', y='amounts'),
      className='figure')


def piechart(names, values):
  return dcc.Graph(
      id='piechart',
      figure=px.pie(names=names, values=values, hole=.9),
      className='figure')


def plan_vs_actual_time_series(budget, actual):
  if budget.empty or actual.empty:
    return html.P('No Data', id='no-data-error')
  actual = actual.set_index('date')
  return dcc.Graph(
      id='plan-vs-actual-time',
      figure=px.line(
          x=actual.index,
          y=actual['amount'].cumsum() / budget['amounts'].sum()),
  )
