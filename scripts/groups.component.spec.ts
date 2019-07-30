/*******************************************************************************
 * # This code is exclusive property of [DB Research Inc.] * # [DB Research
 * Inc.] preserves all the copyrights to sell, * # distribute,license, use,
 * deploy, develop and modify this code as per its requirements. * # Licensee is
 * not supposed to modify,distribute or copy this code. * # Licensees rights are
 * restricted to the use of this as a part of his/her product and * # distribute
 * as a part of his/her product unless otherwise exclusively waved by a written * #
 * contract authorized by [DB Research Inc.] * # Manhattan is the trademark to
 * be displayed with every bundling of this source by the licensee. * # Code has
 * been only exposed to development vendor DBResearchinc/DBR and its staff
 * legally binds * # under NDA and Non-compete as per Minnesota USA Jurisdiction
 * and US copyright law. *
 * #***************************************************************************************************** #
 * Copyright:: 2019, DB Research Inc, All Rights Reserved. * #
 ******************************************************************************/
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupsComponent } from './groups.component';

describe('GroupsComponent', () => {
  let component: GroupsComponent;
  let fixture: ComponentFixture<GroupsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GroupsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
