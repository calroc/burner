import time, mock, dyba

@mock.patch('dyba.Table')
def test_dyba(mock_Table):
  table = mock.Mock()
  table_batch = mock.Mock()
  mock_Table.return_value = table
  table.batch_write.return_value = table_batch
  a = dyba.get_appender('Dummy')
  dyba.write_datum(a, 'tag', 'url')
  a(dyba.DONE)
  time.sleep(2.5)
  for m in (mock_Table, table, table_batch):
    print m.mock_calls

