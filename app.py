import datetime

import dash_daq as daq
import pandas as pd
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output

import figures as figs

app = Dash(__name__, title='Financial Planning and Monitoring')

budget = pd.DataFrame({
    'items': [
        'House', 'Health', 'Groceries', 'Transportation', 'Investing', 'Income',
        'Travel'
    ],
    'amounts': list(range(7))
})

actual = pd.DataFrame(
    {
        'date': datetime.datetime.today().strftime('%Y-%m-%d'),
        'amount': 0.0,
        'description': '',
        'category': ''
    },
    index=[0])


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
          html.H3('Monthly Balance: {}'.format(0.0), id='quick-stats-total'),
          html.Div(
              className='stats',
              children=[
                  html.Div(
                      id='numerical-stats',
                      children=[
                          html.Span(
                              children='Already spent: {}'.format(0.0),
                              className='numerical-stat',
                              id='quick-stats-planned'),
                          html.Span(
                              children='Planned revenue: {}'.format(0.0),
                              className='numerical-stat',
                              id='quick-stats-income')
                      ]),
                  daq.Gauge(
                      id="progress-gauge",
                      size=80,
                      value=0.0,
                      max=1.0,
                      min=0.0,
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
                              'Already spent: {}'.format(0.0),
                              className='numerical-stat',
                              id='item-stats-planned'),
                          html.Span(
                              'Planned income: {}'.format(0.0),
                              className='numerical-stat',
                              id='item-stats-income'),
                      ]),
                  daq.Gauge(
                      id="item-progress-gauge",
                      size=80,
                      value=0.0,
                      max=1.0,
                      min=0.0,
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
              row_deletable=True,
              id='budget-data-table'),
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
              actual.to_dict('records'), [{
                  'name': 'Date',
                  'id': 'date',
                  'type': 'datetime'
              }, {
                  'name': 'Amount',
                  'id': 'amount',
                  'type': 'numeric'
              }, {
                  'name': 'Description',
                  'id': 'description',
                  'type': 'text'
              }, {
                  'name': 'Category',
                  'id': 'category',
                  'type': 'text'
              }],
              editable=True,
              row_deletable=True,
              id='actual-data-table'),
          html.Button('Add Row', className='editing-rows-button', n_clicks=0)
      ])


@app.callback([
    Output('progress-gauge', 'value'),
    Output('progress-gauge', 'max'),
    Output('quick-stats-income', 'children'),
    Output('quick-stats-planned', 'children'),
    Output('quick-stats-total', 'children')
], [Input('actual-data-table', 'data'),
    Input('budget-data-table', 'data')])
def update_stats_panel(actual_data, budget_data):
  planned_total = pd.DataFrame(budget_data)['amounts'].sum()
  # Make sure that plan is not exactly zero as this causes the Guage to freak
  # out
  actual_total = pd.DataFrame(actual_data)['amount'].sum()
  return (actual_total, planned_total or
          planned_total + 1.0, 'Planned income: {}'.format(planned_total),
          'Already spent: {}'.format(actual_total),
          'Monthly Balance: {}'.format(planned_total - actual_total))


@app.callback([
    Output('item-progress-gauge', 'value'),
    Output('item-progress-gauge', 'max'),
    Output('item-stats-income', 'children'),
    Output('item-stats-planned', 'children')
], [
    Input('actual-data-table', 'data'),
    Input('budget-data-table', 'data'),
    Input('dropdown', 'value')
])
def update_budgetary_item_stats_panel(actual_data, budget_data, item):
  budget_data = pd.DataFrame(budget_data)
  actual_data = pd.DataFrame(actual_data)
  planned_total = budget_data[budget_data['items'] == item]['amounts'].sum()
  actual_total = actual_data[actual_data['category'] == item]['amount'].sum()
  # Make sure that plan is not exactly zero as this causes the Guage to freak
  # out
  return (actual_total, planned_total or
          planned_total + 1.0, 'Planned income: {}'.format(planned_total),
          'Already spent: {}'.format(actual_total))


app.layout = html.Div(
    id='app-container',
    children=[
        build_banner(),
        html.Div(
            className='panels',
            children=[
                build_quick_stats_panel(),
                build_budgetary_item_stats_panel(),
                build_timeseries(),
                build_plan_vs_actual_panel(),
                build_piechart(),
                build_budget_table(),
                build_actual_table()
            ])
    ])

if __name__ == '__main__':
  app.run_server(debug=True)
