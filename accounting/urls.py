from django.urls import path
from django.views.generic import TemplateView
from . import currency,chart_of_accounts,fiscal_year,type_of_bank,paymentvoucher,imprest



app_name = 'accounting'

urlpatterns = [
 #Currency start
    path('currency/',currency.currency,name='currency-list'),
    path('currency/new/',currency.add_currency,name='new-currency'),
    path('currency/<str:currenncy_id>/delete/',currency.delete_currency,name='delete-currency'),
    path('currency/upload/',currency.uploads_currency,name='uploads-currency'),
    path('currency/<str:currency_id>/edit/',currency.edit_currency,name='edit-currency'),
 #Currency End
 
 #Chart of Accounts Start
    path('chart-of-accounts/',chart_of_accounts.accountclass,name='accountclass-list'),
    path('chart-of-accounts/new/',chart_of_accounts.add_accountclass,name='new-accountclass'),
    path('chart-of-accounts/<str:accountclass_id>/edit/',chart_of_accounts.edit_accountclass,name='edit-accountclass'),
    path('chart-of-accounts/upload/',chart_of_accounts.uploads_accountclass,name='uploads-accountclass'),
    path('chart-of-accounts/<str:accountclass_id>/delete/',chart_of_accounts.delete_accountclass,name='delete-accountclass'),
    path('chart-of-accounts/<str:accountitem_id>/account-items/',chart_of_accounts.add_accountitem,name='add-accountitem'),
    path('chart-of-accounts/accountitem/<str:accountitem_id>/delete/',chart_of_accounts.delete_accountitem,name='delete-accountitem'),
    path('chart-of-accounts/accountitem/<str:accountitem_id>/edit/',chart_of_accounts.edit_accountitem,name='edit-accountitem'),
    path('chart-of-accounts/<str:accountitem_id>/account-subitems/',chart_of_accounts.add_accountsubitem,name='add-accountsubitem'),
    path('chart-of-accounts/<str:accountsubitem_id>/account-subitems/edit/',chart_of_accounts.edit_accountsubitem,name='edit-accountsubitem'),
    path('chart-of-accounts/<str:accountsubsubitem_id>/account-subsubitems/',chart_of_accounts.add_accountsubsubitem,name='add-accountsubsubitem'),
    path('chart-of-accounts/<str:accountsubsubitem_id>/account-subsubitems/edit/',chart_of_accounts.edit_accountsubsubitem,name='edit-accountsubsubitem'),
    path('chart-of-accounts/item/subiitem/subsubitem/<str:subsubitem_id>/change_status/',chart_of_accounts.change_subsubitemstatus,name='change-subsubitemstatus'),
#Chart of Accounts End

#Fiscal Start
    path('fiscalyear/',fiscal_year.fiscalyear,name='fiscalyear-list'),
    path('fiscalyear/new/',fiscal_year.add_fiscalyear,name='add-fiscalyear'),
    path('fiscalyear/<str:fiscalyear_id>/update/',fiscal_year.edit_fiscalyear,name='edit-fiscalyear'),
    path('fiscalyear/<str:fiscalyear_id>/delete/',fiscal_year.delete_fiscalyear,name='dellete-fiscalyear'),
    path('fiscalyear/<str:fiscalyear_id>/activate/',fiscal_year.activate_fiscalyear,name='activate-fiscalyear'),
    path('fiscalyear/<str:fiscalyear_id>/deactivate/',fiscal_year.deactivate_fiscalyear,name='deactivate-fiscalyear'),
#End Fiscal Year

#Bank Acoounts Type Start
   path('bank/acoounts/type/',type_of_bank.banktype,name='banktype-list'),
   path('bank/acoounts/type/new/',type_of_bank.add_banktype,name='new-banktype'),
   path('bank/acoounts/type/<str:banktypeid_id>/update/',type_of_bank.edit_banktype,name='edit-banktype'),
   path('bank/acoounts/type/<str:banktypeid_id>/delete/',type_of_bank.delete_banktype,name='delete-banktype'),
   path('bank/acoounts/type/upload/',type_of_bank.banktype_upload,name='upload-banktype'),
   path('assign/bank/accounts/type/',type_of_bank.assign_banktype,name='assign-banktype'),
#Bank Acoounts Type End

#Payment Voucher Start

   path('paymentvoucher/',paymentvoucher.manage_paymentvouchers,name='paymentvoucher-list'),
   path('paymentvoucher/ia/',paymentvoucher.ia_paymentvouchers,name='ia-list'),
   path('paymentvoucher/payables/list/',paymentvoucher.payables,name='payables'),
   path('paymentvoucher/pending/',paymentvoucher.pending_paymentvouchers,name='pending-paymentvoucher-list'),
   path('paymentvoucher/authorised/',paymentvoucher.approve_paymentvouchers,name='authorised-paymentvoucher-list'),
   path('paymentvoucher/approved/',paymentvoucher.authorisedpassed_paymentvouchers,name='authorisedandpay-paymentvoucher-list'),
   path('paymentvoucher/cheque/entry/list/',paymentvoucher.checknumber_paymentvouchers,name='chequeno-paymentvoucher-list'),
   path('paymentvoucher/all/',paymentvoucher.all_paymentvouchers,name='all-paymentvoucher-list'),
   path('paymentvoucher/<str:document_id>/new/',paymentvoucher.add_pv,name='new-pv'),
   path('paymentvoucher/new/without-document/',paymentvoucher.add_pv_without_doc,name='new-no-doc-pv'),
   path('paymentvoucher/new/<str:pv_id>/detail/',paymentvoucher.add_pv_detail,name='add-deatil-pv'),
   path('paymentvoucher/<str:pv_id>/detail/',paymentvoucher.pv_detail,name='pv-detail'),
   path('paymentvoucher/<str:pv_id>/update/',paymentvoucher.update_pv,name='edit-update_pv'),
   path('paymentvoucher/detail/item/<str:pvitem_id>/delete/',paymentvoucher.delete_pvitem,name='delete_pvitem'),
   path('paymentvoucher/<str:pv_id>/approve/',paymentvoucher.change_pv_status,name='change-pv-status'),
   path('paymentvoucher/<str:pv_id>/cheque-number/',paymentvoucher.add_cheque_no,name='add-cheque-no'),
   path('paymentvoucher/<str:pv_id>/check-eligibility/',paymentvoucher.check_pv_eligibility,name='check-pv-eligibility'),
   path('paymentvoucher/<str:ia_id>/internal/audit/ledger/',paymentvoucher.ia_detail,name='ia-detail'),
   path('paymentvoucher/detail/<str:attachemnt_id>/attachment/view/',paymentvoucher.view_pvattachment,name='view-pvattachment'),
   path('paymentvoucher/detail/<str:pv_id>/attachment/new/',paymentvoucher.add_pv_attachment,name='add-pv-attachment'),
   path('paymentvoucher/attachemnt/<str:item_id>/remove/', paymentvoucher.remove_pvattachemnt,name='remove-pvattachemnt'),
   path('paymentvoucher/deatil/<str:pv_id>/document/',paymentvoucher.view_pvdocument_detail,name='view-pvdocument-detail'),
   path('paymentvoucher/<str:pv_id>/correction/',paymentvoucher.sendbackto_ia_pvattachemnt,name='sendbackto-ia-pvattachemnt'),
   path('paymentvoucher/<str:pv_id>/document/attachment/<str:attachment_id>/view/',paymentvoucher.view_pvdocattachment,name='view-pvdocattachment'),
   path('paymentvoucher/<str:pv_id>/nofity/payee/',paymentvoucher.notifypayee,name='notifypayee'),
   path('paymentvoucher/<str:pv_id>/cheque/confirm/',paymentvoucher.comfirm_checknumber,name='comfirm-checknumber'),
   path('paymentvoucher/<str:pv_id>/beneficiaries/',paymentvoucher.pull_beneficiaries,name='pull-beneficiaries'),
   path('paymentvoucher/<str:pv_id>/add/beneficiaries/',paymentvoucher.pv_beneficiary_upload,name='pv-beneficiary-upload'),
   path('paymentvoucher/<str:pv_id>/beneficiaries/list/',paymentvoucher.list_pv_beneficiary,name='list-pv-beneficiary'),
   path('paymentvoucher/beneficiary/list/<str:item_id>/comfirm/',paymentvoucher.comfirm_code,name='comfirm-code'),
   path('paymentvoucher/beneficiary/list/<str:item_id>/comfirm/code/resend/',paymentvoucher.resend_code,name='resend-code'),
   path('paymentvoucher/beneficiarylist/<str:item_id>/pay/',paymentvoucher.make_payment,name='make-payment'),
   
#Payment Voucher End

#Imprest Start
   path('imprest/',imprest.manage_imprest,name='manage-imprest'),
   path('imprest/pending/',imprest.pending_imprest,name='pending-imprest'),
   path('imprest/approved/',imprest.approved_imprest,name='approved-imprest'),
   path('imprest/certified/',imprest.certified_imprest,name='certified-imprest'),
   path('imprest/retire/',imprest.retire_imprest,name='retire-imprest'),
   path('imprest/new/',imprest.add_imprest,name='add-imprest'),
   path('imprest/<str:imprest_id>/',imprest.imprest_detail,name='imprest-detail'),
   path('imprest/<str:imprest_id>/update/',imprest.edit_imprest,name='edit-imprest'),
   path('imprest/<str:imprest_id>/approve/',imprest.imprest_change_status,name='imprest-change-status'),
   path('imprest/<str:imprest_id>/close/',imprest.notifyhod,name='imprest-notifyhod-close'),
   path('imprest/<str:imprest_id>/actualexpense/',imprest.add_imprest_expense,name='add-imprest-expense')

#Imprest End 
]