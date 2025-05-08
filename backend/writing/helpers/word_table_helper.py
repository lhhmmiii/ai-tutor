import pandas as pd


def extract_text_from_table(table):
    table_data = []
    for j in range(0, table.Rows.Count):
        row_data = []
        for k in range(0, table.Rows.get_Item(j).Cells.Count):
            cell = table.Rows.get_Item(j).Cells.get_Item(k)
            cell_text = ""
            for para in range(cell.Paragraphs.Count):
                paragraph_text = cell.Paragraphs.get_Item(para).Text
                cell_text += paragraph_text + " "
            row_data.append(cell_text)
        table_data.append(row_data)
    df = pd.DataFrame(table_data, index=None)
    table_text = df.to_string(index=False, header=False)

    return table_text
