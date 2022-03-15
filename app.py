import datetime

import dash_daq as daq
import pandas as pd
import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import figures as figs
import utils

app = Dash(__name__, title='Financial Planning and Monitoring')


def init_tables():
  budget = pd.DataFrame({
      'items': [
          'House', 'Health', 'Groceries', 'Transportation', 'Investing',
          'Income', 'Travel'
      ],
      'amounts': list(range(7))
  })
  actual = pd.DataFrame(
      {
          'date': [datetime.datetime.today().strftime('%Y-%m-%d')],
          'amount': [0.0],
          'description': ['Add description...'],
          'category': ['']
      },
      index=[0])
  return budget, actual


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
          html.H4('Bottom Line'),
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
              ]),
          html.H3('Monthly Balance: {}'.format(0.0), id='quick-stats-total'),
      ])


def build_budgetary_item_stats_panel():
  budget, _ = init_tables()
  return html.Div(
      id='item-quick-stats',
      className='panel',
      children=[
          html.H4('Bottom Line per Item'),
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
                              'Planned amount: {}'.format(0.0),
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
              ]),
          dcc.Dropdown(budget['items'], budget['items'].iloc[0], id='dropdown')
      ])


def build_plan_vs_actual_panel():
  budget, actual = init_tables()
  return html.Div(
      id='plan-vs-actual',
      className='panel',
      children=[
          html.H4('Planned vs. Actual'),
          dcc.Graph(
              id='plan-vs-actual-all-budgetary-items',
              figure=figs.plan_vs_actual_fig(budget, actual),
              className='figure')
      ])


def build_piechart():
  return html.Div(
      id='piechart-panel',
      className='panel',
      children=[
          html.H4('Budgetary Items Distribution'),
          dcc.Graph(id='piechart', className='figure')
      ])


def build_timeseries():
  budget, actual = init_tables()
  return html.Div(
      id='timeseries',
      className='panel',
      children=[
          html.H4('Planned vs. Actual Through Time'),
          dcc.Graph(
              id='plan-vs-actual-time',
              figure=figs.plan_vs_actual_time_series(budget, actual))
      ])


def build_budget_table():
  budget, _ = init_tables()
  return html.Div(
      className='panel',
      id='budget-table',
      children=[
          html.H4('Budget'),
          dash_table.DataTable(
              budget.to_dict('records'), [{
                  'name': 'Items',
                  'id': 'items',
                  'type': 'text'
              }, {
                  'name': 'Amount',
                  'id': 'amounts',
                  'type': 'numeric',
              }],
              editable=True,
              row_deletable=True,
              id='budget-data-table'),
          html.Button('Add Row', id='budget-rows-button', n_clicks=0)
      ])


def build_actual_table():
  budget, actual = init_tables()
  return html.Div(
      className='panel',
      id='actual-table',
      children=[
          html.H4('Actual'),
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
                  'type': 'text',
                  'presentation': 'dropdown'
              }],
              editable=True,
              row_deletable=True,
              dropdown={
                  'category': {
                      'options': [{
                          'label': i,
                          'value': i
                      } for i in budget['items'].unique()]
                  }
              },
              style_cell={
                  'overflow': 'hidden',
                  'textOverflow': 'ellipsis',
                  'maxWidth': 0,
              },
              tooltip_data=[{
                  column: {
                      'value': str(value),
                      'type': 'markdown'
                  } for column, value in row.items() if column == 'category'
              } for row in actual.to_dict('records')],
              tooltip_duration=None,
              style_table={
                  'height': '20em',
                  'overflowY': 'auto'
              },
              id='actual-data-table'),
          html.Button('Add Row', id='actual-rows-button', n_clicks=0)
      ])


@app.callback(
    Output('actual-data-table', 'tooltip_data'),
    Input('actual-data-table', 'data'))
def update_actual_table_tooltips(table_data):
  actual_total = utils.table_data_to_frame(table_data)
  return [{
      column: {
          'value': str(value),
          'type': 'markdown'
      } for column, value in row.items() if column != 'category'
  } for row in actual_total.to_dict('records')]


@app.callback([
    Output('progress-gauge', 'value'),
    Output('progress-gauge', 'max'),
    Output('quick-stats-income', 'children'),
    Output('quick-stats-planned', 'children'),
    Output('quick-stats-total', 'children')
], [Input('actual-data-table', 'data'),
    Input('budget-data-table', 'data')])
def update_stats_panel(actual_data, budget_data):
  planned_total = utils.table_data_to_frame(budget_data)['amounts'].sum()
  # Make sure that plan is not exactly zero as this causes the Guage to freak
  # out
  actual_total = utils.table_data_to_frame(actual_data)['amount'].sum()
  return (actual_total, planned_total or
          planned_total + 1.0, 'Planned amount: {}'.format(planned_total),
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
  budget_data = utils.table_data_to_frame(budget_data)
  actual_data = utils.table_data_to_frame(actual_data)
  planned_total = budget_data[budget_data['items'] == item]['amounts'].sum()
  actual_total = actual_data[actual_data['category'] == item]['amount'].sum()
  # Make sure that plan is not exactly zero as this causes the Guage to freak
  # out
  return (actual_total, planned_total or
          planned_total + 1.0, 'Planned amount: {}'.format(planned_total),
          'Already spent: {}'.format(actual_total))


@app.callback(Output('piechart', 'figure'), Input('budget-data-table', 'data'))
def update_piechart(budget_data):
  budget_data = utils.table_data_to_frame(budget_data)
  return figs.piechart(budget_data['items'], budget_data['amounts'])


@app.callback(
    Output('plan-vs-actual-all-budgetary-items', 'figure'),
    [Input('actual-data-table', 'data'),
     Input('budget-data-table', 'data')])
def update_budget_vs_planned(actual_data, budget_data):
  budget_data = utils.table_data_to_frame(budget_data)
  actual_data = utils.table_data_to_frame(actual_data)
  return figs.plan_vs_actual_fig(budget_data, actual_data)


@app.callback(
    Output('plan-vs-actual-time', 'figure'),
    [Input('actual-data-table', 'data'),
     Input('budget-data-table', 'data')])
def update_timeseries(actual_data, budget_data):
  budget = utils.table_data_to_frame(budget_data)
  actual = utils.table_data_to_frame(actual_data)
  try:
    fig = figs.plan_vs_actual_time_series(budget, actual)
    return fig
  except Exception:
      raise PreventUpdate


@app.callback(
    Output('local-storage', 'data'),
    [Input('budget-data-table', 'data'),
     Input('actual-data-table', 'data')], State('local-storage', 'data'))
def update_cache(budget_table_data, actual_table_date, storage):
  if storage is None:
    budget, actual = init_tables()
    data = {'budget': budget.to_dict(), 'actual': actual.to_dict()}
  else:
    data = storage
  data['budget'] = budget_table_data
  data['actual'] = actual_table_date
  return data


@app.callback(
    [Output('budget-data-table', 'data'),
     Output('actual-data-table', 'data')], [
         Input('local-storage', 'modified_timestamp'),
         Input('actual-rows-button', 'n_clicks'),
         Input('budget-rows-button', 'n_clicks')
     ], State('local-storage', 'data'), State('actual-data-table', 'data'),
    State('actual-data-table', 'columns'), State('budget-data-table', 'data'),
    State('budget-data-table', 'columns'))
def on_data_set_table(ts, actual_n_clicks, budget_n_clicks, storage,
                      actual_rows, actual_columns, budget_rows, budget_columns):
  if ts is None or storage is None:
    raise PreventUpdate
  ctx = dash.callback_context
  input_id = ctx.triggered[0]["prop_id"].split(".")[0]
  if input_id == 'actual-rows-button' and actual_n_clicks > 0:
    defaults = {'datetime': datetime.datetime.today().strftime('%Y-%m-%d'),
                'text': 'Add description...',
                'numeric': 0.0}
    actual_rows.append({c['id']: defaults[c['type']] for c in actual_columns})
    storage['actual'] = actual_rows
  if input_id == 'budget-rows-button' and budget_n_clicks > 0:
    defaults = {'datetime': datetime.datetime.today().strftime('%Y-%m-%d'),
                'text': '',
                'numeric': 0.0}
    budget_rows.append({c['id']: defaults[c['type']] for c in budget_columns})
    storage['budget'] = budget_rows
  return storage['budget'], storage['actual']


app.layout = html.Div(
    id='app-container',
    children=[
        build_banner(),
        html.Div(
            className='panels',
            children=[
                dcc.Store(id='local-storage', storage_type='local'),
                build_quick_stats_panel(),
                build_budgetary_item_stats_panel(),
                build_timeseries(),
                build_plan_vs_actual_panel(),
                build_piechart(),
                build_budget_table(),
                build_actual_table(),
                html.Div(id='dummy-div', style={'display': 'none'})
            ])
    ])

if __name__ == '__main__':
  app.run_server(debug=True)
