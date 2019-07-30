/*****************************************************************************************
#This code is exclusive property of [DB Research Inc.].
#[DB Research Inc.] preserves all the copyrights to sell,
#distribute,license, use, deploy, develop and modify this code as per its requirements.
#Licensee is not supposed to modify,distribute or copy this code.
#Licensees rights are restricted to the use of this as a part of his/her product and
#distribute as a part of his/her product unless otherwise exclusively waved by a written
#contract authorized by  [DB Research Inc.] .
#Manhattan is the trademark to be displayed with every bundling of this source by the licensee.
#Code has been only exposed to development vendor DBResearchinc/DBR and its staff legally binds
#under NDA and Non-compete as per Minnesota USA Jurisdiction and US copyright law.
#******************************************************************************************/
/*		Copyright:: 2019, DB Research Inc, All Rights Reserved.   	  	  				  */
/*****************************************************************************************/
package com.dbr.manhattan.master.ldap.service;

import java.util.List;

import javax.naming.Name;

import com.dbr.manhattan.master.model.GroupResponse;
import com.dbr.manhattan.master.model.PostGroupRequest;

/**
 * This interface is for group service
 * 
 * @author Rajesh
 *
 */
public interface GroupService {
	/**
	 * Find groups
	 * 
	 * @author Rajesh
	 * @return {@link List GroupResponse}
	 */
	public List<GroupResponse> findAll();

	/**
	 * Find group
	 * 
	 * @author Rajesh
	 * @param group
	 * @return {@link GroupResponse}
	 */
	public GroupResponse getGroupInformation(String group);

	/**
	 * Create a new group
	 * 
	 * @author Rajesh
	 * @param group
	 */
	public void create(PostGroupRequest group);

	/**
	 * Delete group
	 * 
	 * @author Rajesh
	 * @param group
	 */
	public void delete(String group);

	/**
	 * Add user to group
	 * 
	 * @author Rajesh
	 * @param groupName
	 * @param user
	 */
	public void assignedUserToGroup(String groupName, String user);

	/**
	 * Remove user from group
	 * 
	 * @author Rajesh
	 * @param groupName
	 * @param user
	 */
	public void removeUserFromGroup(String groupName, String user);

	/**
	 * Delete groups
	 * 
	 * @author Rajesh
	 */
	public void deleteGroups();

	/**
	 * List groups of user
	 * 
	 * @author Rajesh
	 * @param user
	 * @return {@link List String}
	 */
	public List<String> userGroups(String user);

	/**
	 * Find user group names
	 * 
	 * @param user
	 * @return {@link List String}
	 */
	public List<String> userGroupsName(String user);

	public List<String> getMembershipGroupName(String userDN);

	public void removeMemberFromGroup(String groupName, String user);

	public Name buildGroupDn(String groupName);
}
