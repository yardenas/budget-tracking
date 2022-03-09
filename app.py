import datetime

import dash_daq as daq
import pandas as pd
from dash import Dash, html, dcc, dash_table

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

actual = actual.set_index('date')


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
              className='stats',
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
                      min=0,
                      showCurrentValue=True)
              ])
      ])


def build_budgetary_item_stats_panel():
  return html.Div(
      id='item-quick-stats',
      className='panel',
      children=[
          html.H4('Budgetary Item Planned vs. Actual'),
          dcc.Dropdown(budget['items'], budget['items'].iloc[0], id='dropdown'),
          html.Div(
              className='stats',
              children=[
                  html.Div(
                      id='item-numerical-stats',
                      children=[
                          html.Span(
                              'Already spent: {}'.format(100),
                              className='numerical-stat'),
                          html.Span(
                              'Planned income: {}'.format(123),
                              className='numerical-stat'),
                      ]),
                  daq.Gauge(
                      id="item-progress-gauge",
                      size=100,
                      value=(23 / 123) * 100.0,
                      max=100,
                      min=0,
                      showCurrentValue=True)
              ])
      ])


def build_plan_vs_actual_panel():
  return html.Div(
      id='plan-vs-actual',
      className='panel',
      children=[html.H4('Planned vs. Actual'),
                figs.plan_vs_actual_fig(budget)])


def build_piechart():
  return html.Div(
      id='piechart-panel',
      className='panel',
      children=[
          html.H4('Budgetary Items Distribution'),
          figs.piechart(budget['items'], budget['amounts'])
      ])


def build_timeseries():
  return html.Div(
      id='timeseries',
      className='panel',
      children=[
          html.H4('Planned vs. Actual Through Time'),
          figs.plan_vs_actual_time_series(budget, actual)
      ])


def build_budget_table():
  return html.Div(
      className='panel',
      id='budget-table',
      children=[
          html.H4('Budget'),
          html.Div([
              dcc.Input(
                  className='adding-rows-name',
                  placeholder='Enter a column name...',
                  value=''),
              html.Button(
                  'Add Column', className='adding-rows-button', n_clicks=0)
          ]),
          dash_table.DataTable(
              budget.to_dict('records'), [{
                  "name": i.capitalize(),
                  "id": i
              } for i in budget.columns],
              editable=True,
              row_deletable=True),
          html.Button('Add Row', className='editing-rows-button', n_clicks=0)
      ])


def build_actual_table():
  return html.Div(
      className='panel',
      id='actual-table',
      children=[
          html.H4('Actual'),
          html.Div([
              dcc.Input(
                  className='adding-rows-name',
                  placeholder='Enter a column name...',
                  value=''),
              html.Button(
                  'Add Column', className='adding-rows-button', n_clicks=0)
          ]),
          dash_table.DataTable(
              budget.to_dict('records'), [{
                  "name": i.capitalize(),
                  "id": i
              } for i in budget.columns],
              editable=True,
              row_deletable=True),
          html.Button('Add Row', className='editing-rows-button', n_clicks=0)
      ])


app.layout = html.Div(
    id='app-container',
    children=[
        build_banner(),
        html.Div(
            className='panels',
            children=[
                build_quick_stats_panel(),
                build_timeseries(),
                build_budgetary_item_stats_panel(),
                build_plan_vs_actual_panel(),
                build_piechart(),
                build_budget_table(),
                build_actual_table()
            ])
    ])

if __name__ == '__main__':
  app.run_server(debug=True)
