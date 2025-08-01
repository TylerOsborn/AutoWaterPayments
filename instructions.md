# Requirements

I would like to create a python script that will be executed by a cron job running on a raspberry pi. The script should execute the following steps:

1. At 00h01 on the first of every month pay R500 into a benificiary account with the sub steps:
   a. Navigate to https://onlinebanking.standardbank.co.za/#/landing-page
   b. Click the sign in button
   c. input the environment variables "STANDARD_BANK_USERNAME" and "STANDARD_BANK_PASSWORD" into the respective fields
   d. Click the following button

   ```html
   <button
     color="tertiary"
     class="tertiary icon-button-link"
     id="Transact-Pay"
     title="Pay"
     ng-click="payDropDown.show = !payDropDown.show;"
   >
     <span class="title title-fix-basics">PAY&nbsp;&nbsp;<i class="icon icon-caret-down"></i></span>
   </button>
   ```

   e. Click the "Beneficiary" drop down that appears
   f. Search for "enbaya" in the with the following html being the input field:

   ```html
   <input
     type="text"
     id="filter"
     name="filter"
     ng-model="query.value"
     ng-change="beneficiary.confirmDelete=false;beneficiary.showExpandedContent=false;beneficiary.deleteFailure=false;"
     placeholder="Search by name, reference, group, date or amount"
     ng-class="{'show-nosearch-results-styles': (query.value != '' &amp;&amp; (beneficiaries|beneficiaryFilter:query.value:!addingGroup).length === 0),
                                               'show-search-results-styles': (query.value != '' &amp;&amp; (beneficiaries|beneficiaryFilter:query.value:!addingGroup).length &gt; 0)}"
     class="ng-pristine ng-valid ng-empty ng-touched"
     style=""
   />
   ```

   g. Click the following html element:

   ```html
   <a
     title="pay"
     class="action pay"
     ng-click="payBeneficiary(beneficiary);$event.stopPropagation();"
     data-dtmid="link_content_list of beneficiaries"
     data-dtmtext="pay icon click"
     ><i class="ibr-icon ibr-icon-pay"></i
   ></a>
   ```

   h. Input "500" into the following input field:

   ```html
   <input
     id="amount"
     type="tel"
     name="Amount"
     input-name=""
     size="12"
     ng-model="ngModel"
     placeholder="0.00"
     class="currency ng-pristine ng-isolate-scope ng-empty ng-invalid ng-invalid-required ng-touched"
     limits=""
     enforcer="enforcer"
     hinter="hinter"
     hint-watcher="hintWatcher"
     ng-disabled="ngDisabled"
     ng-change="timeoutChange(ngChange)"
     ng-blur="timeoutChange(ngBlur)"
     ng-class="ngClass"
     max=""
     min=""
     required=""
     label="Amount"
     style=""
   />
   ```

   i. Click the "Next" button:

   ```html
   <button
     _ngcontent-vsb-c0=""
     class="primary primary__default none"
     type="submit"
     data-dtmtext="step 1 | next button click"
     data-dtmid="link_content_pay single beneficiary"
   >
     <ng-transclude></ng-transclude>Next
   </button>
   ```

   g. Click the confirm button:

   ```html
   <button
     _ngcontent-vsb-c0=""
     class="primary primary__default none"
     type="button"
     data-dtmtext="step 2 | confirm button click"
     data-dtmid="link_content_pay single beneficiary"
   >
     <ng-transclude></ng-transclude>Confirm
   </button>
   ```

   h. Take a screenshot of the resulting page

2. Sleep for 7 minutes

3. Send an SMS with a free service that can use South African numbers. Either a new generated number or preferably able to take an existing number so that I can input my phone number into the following env variable "PHONE_NUMBER_USER". The sms should be sent to a number stored in the environment variable "PHONE_NUMBER_ENBAYA" and have the following content "2367*0120240822367*500"

4. (Optional) If the sms service used does not allow for existing numbers to be used then I would like the program to wait for an SMS and then forward the text content to the number stored in "PHONE_NUMBER_USER"
