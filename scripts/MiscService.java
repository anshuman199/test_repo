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
package com.dbr.manhattan.master.service;

import com.dbr.manhattan.master.model.AboutResponse;


/**
 * This interface is for miscellaneous
 * 
 * @author Rajesh
 *
 */
public interface MiscService {
	/**
	 * Read hash code from manhattahash file
	 * 
	 * @author Rajesh
	 * @return {@link AboutResponse}
	 */
	public AboutResponse getAboutSectionData();
}
