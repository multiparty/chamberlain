def show_computation_form():
    return '''
           <form method="POST" enctype="application/json">
               <div><label>computation_id: <input type="text" name="computation_id"></label></div>
               <div><label>party_count: <input type="number" name="party_count"></label></div>
               <div><label>party_list: <input type="text" name="party_list"></label></div>
               <div><label>data_set_id: <input type="text" name="data_set_id"></label></div>
               <div><label>workflow_id: <input type="text" name="workflow_id"></label></div>
               <input type="submit" value="Submit">
           </form>'''


