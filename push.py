import time, mock, dyba

@mock.patch('dyba.Table')
def test_dyba(mock_Table):
  mock_Table.return_value = table = mock.Mock(name='table')
  table.batch_write.return_value = table_batch = mock.MagicMock(name='batch')
  table_batch.__enter__.return_value = ent = mock.Mock(name='enter')
  ent.put_item = pi = mock.Mock(name='put_item')

  a = dyba.get_appender('Dummy')
  dyba.write_datum(a, 'tag', 'url')
  a(dyba.DONE)
  time.sleep(2.5)

  ret = mock_Table, table, table_batch, ent, pi
  for m in ret:
    print m.mock_calls
  return ret


T, t, b, e, p = test_dyba()

