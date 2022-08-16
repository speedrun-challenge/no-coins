import {HttpClient} from '@angular/common/http';
import {Component, OnInit} from '@angular/core';
import {ENTRIES} from './entries';
import {UPDATE_TIME} from './update-time';

export interface Entry {
  position: number;
  name: string;
  id: string;
  rank_sum: number;
  subsurf_rank: number;
  subsurf_t: number;
  tr2_rank: number;
  tr2_t: number;
}

interface VisitorResponse {
  visitorsMonth: number
  visitorsTotal: number
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  public displayedColumns: string[] = ['position', 'name', 'rank_sum', 'subsurf_rank', 'subsurf_t', 'tr2_rank', 'tr2_t'];
  public entries: Entry[] = ENTRIES;
  public updateTime: string = UPDATE_TIME;
  public visitors?: VisitorResponse;

  public constructor(private readonly http: HttpClient) {
  }

  public ngOnInit(): void {
    this.fetchVisitorCount();
  }

  private fetchVisitorCount(): void {
    this.http.get<VisitorResponse>('https://akleemans.pythonanywhere.com/api/visitors')
    .subscribe(visitorResponse => this.visitors = visitorResponse);
  }
}
