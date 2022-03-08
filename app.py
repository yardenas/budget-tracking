import datetime

import dash_daq as daq
import pandas as pd
from dash import Dash, html

import figures as figs

app = Dash(__name__, title='Financial Planning and Monitoring')

budget = pd.DataFrame({
    'items': [
        'House', 'Health', 'Groceries', 'Transportation', 'Investing', 'Income',
        'Travel'
    ],
    'amounts': list(range(7))
})

actual = pd.DataFrame({
    'date': pd.Series(dtype='datetime64[ns]'),
    'amount': pd.Series(dtype=float),
    'description': pd.Series(dtype=str),
    'category': pd.Series(dtype=str)
})


def build_banner():
  return html.Header(children=[
      html.H1('Yarden\'s Finance Dashboard'),
      html.H2(datetime.datetime.now().strftime("%d, %b %Y"))
  ])


def build_quick_stats_panel():
  return html.Div(
      id='quick-stats',
      className='panel',
      children=[
          html.H3('Monthly Balance: {}'.format(23)),
          html.Div(
              id='stats',
              children=[
                  html.Div(
                      id='numerical-stats',
                      children=[
                          html.Span(
                              'Already spent: {}'.format(100),
                              className='numerical-stat'),
                          html.Span(
                              'Planned income: {}'.format(123),
                              className='numerical-stat')
                      ]),
                  daq.Gauge(
                      id="progress-gauge",
                      size=100,
                      value=(23 / 123) * 100.0,
                      max=100,
                      min=0)
              ])
      ])


def build_plan_vs_actual_panel():
  return html.Div(
      id='plan-vs-actual',
      className='panel',
      children=[
          html.H4('Budgetary Items Planned vs. Actual'),
          figs.plan_vs_actual_fig(budget)
      ])


def build_piechart():
  return html.Div(
      id='piechart-panel',
      className='panel',
      children=[
          html.H4('Budgetary Items Distribution'),
          figs.piechart(budget['items'], budget['amounts'])
      ])


app.layout = html.Div(
    id='app-container',
    children=[
        build_banner(),
        html.Div(
            className='panels',
            children=[
                build_quick_stats_panel(),
                build_plan_vs_actual_panel(),
                build_piechart()
            ])
    ])

if __name__ == '__main__':
  app.run_server(debug=True)
