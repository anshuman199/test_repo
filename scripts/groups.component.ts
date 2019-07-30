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
import { AdminService } from './../services/admin.service';
import { Component, OnInit } from '@angular/core';
import { GroupsService } from '../services/groups.service';
import { ConstantPointsService } from '../services/constant-points.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.css']
})
export class GroupsComponent implements OnInit {

  public groupDetails = [];
  public usersList = [];
  public addGroupResponse = [];
  public deleteGroupResponse = [];

  public config: any;
  public dataBody: any;

  public deleteMultipleGroupResponse = [];
  public deleteMultipleGroupsResponse = [];
  public groupItemListArray = [];
  public newArrayToDeleteMultipleGroup = [];
  public newArrayToDeleteSingleGroup = [];

  public checkAll: boolean = false;
  public disableDeleteButtonForGroup: boolean = true;

  public showMultipleDeleteButton: boolean = false;

  public messageClass: string;
  public showResponseMessageBox: boolean = false;
  public responseMessage: string;


  public addNewGroupForm: FormGroup;
  public submitted: boolean = false;

  public ui_li_add_new_group_tab: boolean;
  public ui_li_list_group_tab: boolean;

  public groupTabSelection: string;

  public maxSize: number = 5;
  public directionLinks: boolean = true;
  public autoHide: boolean = true;
  public responsive: boolean = true;
  public labels: any = {
    previousLabel: '',
    nextLabel: '',
  };

  public dropdownSettings = {};

  constructor(private data: GroupsService, private baseUrlVar: ConstantPointsService, private formBuilder: FormBuilder,
    private adminservice: AdminService, public loginService: AuthenticationService) {
    this.config = {
      itemsPerPage: 5,
      currentPage: 1,
      totalItems: this.groupDetails.length
    };
  }

  pageChanged(event) {
    this.config.currentPage = event;
  }

  ngOnInit() {

    this.ui_li_list_group_tab = true;
    this.ui_li_add_new_group_tab = false;
    this.groupTabSelection = 'listTabOfAdminOrUser';

    this.groupListFunction();
    this.userListFunction();
    this.formFieldOfAddNewGroupRefreshFunction();

  }

  formFieldOfAddNewGroupRefreshFunction() {

    this.submitted = false;

    this.addNewGroupForm = this.formBuilder.group({
      groupname: ['', [Validators.required, Validators.maxLength(50)]],
      selectedUser: ['', [Validators.required]]
    });
  }

  // Function to show the response message when API is called
  showResponseMessageFunction(addMessageClass, addMessageData, toShowMessage) {

    this.messageClass = addMessageClass;
    this.responseMessage = addMessageData;
    this.showResponseMessageBox = toShowMessage;
  }

  // Function to close the meesgae box in a html page or view page
  closeMessageBoxFunction() {
    this.showResponseMessageFunction('', '', false);
  }

  // convenience getter for easy access to form fields or Getter method to access formcontrols
  get field() {
    return this.addNewGroupForm.controls;
  }

  // Function to submit the information from add a new group form
  onSubmit() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.addNewGroupForm.invalid) {
      return;
    }

    this.addNewGroupFunction();
    this.formFieldOfAddNewGroupRefreshFunction();
  }

  addNewGroupFunction() {

    this.dataBody = {
      "name": this.addNewGroupForm.value.groupname,
      "members": this.addNewGroupForm.value.selectedUser
    };

    this.data.addNewGroup(this.baseUrlVar.baseUrl, this.dataBody).subscribe((data) => {
      this.addGroupResponse = data;
      this.showResponseMessageFunction('success', data.message, true);
      this.formFieldOfAddNewGroupRefreshFunction();
      this.groupListFunction();
    })
  }

  // Function to switching the tabs in a html page 
  switchTabFunction(value) {

    if (value == 'listTabOfGroup') {

      this.ui_li_list_group_tab = true;
      this.ui_li_add_new_group_tab = false;
      this.groupTabSelection = 'listTabOfGroup';
    }
    else if (value == 'addnewGroup') {

      this.ui_li_list_group_tab = false;
      this.ui_li_add_new_group_tab = true;
      this.groupTabSelection = 'addnewGroup';
    }

  }

  // Function to get the list of the users
  userListFunction() {

    this.adminservice.getListOfUsers(this.baseUrlVar.baseUrl).subscribe((data) => {

      for (var i = 0; i < data.length; i++) {
        this.usersList.push(data[i].uid);
      }

      this.dropdownSettings = {
        singleSelection: false,
        selectAllText: 'Select All',
        unSelectAllText: 'UnSelect All',
        itemsShowLimit: 5,
        allowSearchFilter: true,
        clearSearchFilter: true
      };
    })
  }

  // Function to get the list of the groups
  groupListFunction() {

    this.data.getListOfGroups(this.baseUrlVar.baseUrl).subscribe(
      (data) => {
        this.groupDetails = data;
      }
    )
  }

  // Functions to delete single group
  showConfirmationWhenDeleteGroupFunction(item) {
    item.confirm = true;
  }

  cancelConfirmationWhenDeleteGroupFunction(item) {
    item.confirm = false;
  }

  deleteGroupFunction(item) {
    this.data.deleteGroup(this.baseUrlVar.baseUrl, item.dn).subscribe((data) => {
      this.deleteGroupResponse = data;
      this.showResponseMessageFunction('success', data.message, true);
      this.groupListFunction();
    })
  }

  // Functions to delete multiple groups

  
  showConfirmationWhenMultipleDeleteFromCheckboxFunction() {
    this.showMultipleDeleteButton = true;
  }

  cancelConfirmationWhenMultipleDeleteFromCheckboxFunction() {
    this.checkAll = false;
    this.disableDeleteButtonForGroup = true;
    this.showMultipleDeleteButton = false;
  }

  getCheckedGroupsFunction(CheckedList) {

    if (typeof CheckedList == 'boolean') {

      if (CheckedList == false) {

        this.newArrayToDeleteMultipleGroup = this.groupItemListArray;

        this.disableDeleteButtonForGroup = false;
      }
      else {
        this.disableDeleteButtonForGroup = true;
      }
      console.log(this.newArrayToDeleteMultipleGroup);
    }
    else if (typeof CheckedList == 'string') {

      var position = this.newArrayToDeleteSingleGroup.indexOf(CheckedList);
      if (position == -1) {
        this.newArrayToDeleteSingleGroup.push(CheckedList);
      }
      else {
        this.newArrayToDeleteSingleGroup.splice(position, 1);
      }

      if (this.newArrayToDeleteSingleGroup.length > 0) {
        this.disableDeleteButtonForGroup = false;
      }
      else {
        this.disableDeleteButtonForGroup = true;
      }
      console.log(this.newArrayToDeleteSingleGroup);
    }
  }

  deleteMultipleGroupFunction(checkAll) {

    if (checkAll) {

      this.data.deleteMultipleGroup(this.baseUrlVar.baseUrl, this.newArrayToDeleteMultipleGroup).subscribe((data) => {
        this.deleteMultipleGroupResponse = data;
        this.showResponseMessageFunction('success', data.message, true);
        this.groupListFunction();

        this.disableDeleteButtonForGroup = true;
        this.showMultipleDeleteButton = false;
      })
    }
    else {

      this.data.deleteMultipleGroup(this.baseUrlVar.baseUrl, this.newArrayToDeleteSingleGroup).subscribe((data) => {
        this.deleteMultipleGroupResponse = data;
        this.showResponseMessageFunction('success', data.message, true);
        this.groupListFunction();

        this.disableDeleteButtonForGroup = true;
        this.showMultipleDeleteButton = false;
      })
    }
  }
}
