import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-cardinals',
  templateUrl: './cardinals.page.html',
  styleUrls: ['./cardinals.page.scss'],
})
export class CardinalsPage implements OnInit {

  private rows: any;

  private columns = [
    { name: 'Cardinal ID', prop: 'cardinalId'},
    { name: 'Cardinal IP', prop: 'cardinalIp'},
    { name: 'Description', prop: 'description'}
  ];

  constructor(
    private http: HttpService
  ) { }

  async ngOnInit() {

    let cardinals;

    const cardinalResponse = await this.http.getAllCardinals().toPromise();
    if (!cardinalResponse.error) {
      cardinals = cardinalResponse.cardinals;
    }

    this.rows = this.formatTableData(cardinals);
    console.log(this.rows);
  }


  formatTableData(cardinals) {
    // Cardinal ID | Cardinal IP | Description
    console.log(cardinals);
    const uniqueIds = [...new Set(cardinals.map(ds => ds[0]))];
    const objects = [];

    for (const cardinal of cardinals) {
      objects.push(
        {
          cardinalId: cardinal[0],
          cardinalIp: cardinal[1],
          description: cardinal[2],
        }
      );
    }
    return objects;
  }

}
