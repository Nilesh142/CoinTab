#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[43]:


X_order_report = pd.read_excel("Company X - Order Report.xlsx")
X_pincode_zones = pd.read_excel("Company X - Pincode Zones.xlsx")
X_SKU_master = pd.read_excel("Company X - SKU Master.xlsx")
Courier_Invoice = pd.read_excel("Courier Company - Invoice.xlsx")
Courier_Rates = pd.read_excel("Courier Company - Rates.xlsx")


# In[44]:


X_SKU_master['SKU'].value_counts()


# In[45]:


X_SKU_master = X_SKU_master.drop_duplicates()
X_SKU_master['SKU'].value_counts()


# In[46]:


X_order_report.info()


# In[47]:


X_pincode_zones.head()


# In[48]:


X_SKU_master.head()


# In[49]:


X_order_report['ExternOrderNo'].value_counts().head(10)


# In[50]:


Courier_Invoice.info()


# In[51]:


Courier_Invoice['AWB Code'].value_counts()


# In[52]:


X_merged = pd.merge(X_order_report, X_SKU_master, on='SKU')


# In[53]:


X_merged['SKU'].value_counts()


# In[37]:


X_merged[X_merged['ExternOrderNo']==2001827036]


# In[58]:


X_merged['Total WT'] = X_merged['Order Qty'] * X_merged['Weight (g)']


# In[64]:


X_merged[X_merged['ExternOrderNo'] == 2001806210]


# In[61]:


X_total_wts = X_merged.groupby('ExternOrderNo').sum()


# In[62]:


X_total_wts


# In[66]:


X


# In[71]:


Courier_Invoice['Pincodes_Merged'] = Courier_Invoice['Warehouse Pincode'].astype('str')+'_' + Courier_Invoice['Customer Pincode'].astype('str')


# In[72]:


Courier_Invoice


# In[73]:


X_pincode_zones['Pincodes_Merged'] = X_pincode_zones['Warehouse Pincode'].astype('str')+'_' + X_pincode_zones['Customer Pincode'].astype('str')


# In[82]:


X_pincode_zones = X_pincode_zones.drop_duplicates()


# In[92]:


master_df = pd.merge(Courier_Invoice, X_pincode_zones, on='Pincodes_Merged', suffixes=('_cc','_xc'))


# In[93]:


master_df[master_df['AWB Code']==1091119169701]


# In[94]:


master_df


# In[99]:


X_total_wts.reset_index(inplace=True)


# In[100]:


X_total_wts.info()


# In[102]:


master_df = pd.merge(master_df,X_total_wts, left_on='Order ID', right_on='ExternOrderNo')


# In[104]:


def get_slabs(wt):
    if wt%500==0:
        return wt
    wt = (wt//500 + 1)*500
    return wt


# In[109]:


master_df['Slab WT'] = master_df['Total WT'].apply(get_slabs)/1000


# In[114]:


master_df


# In[115]:


def get_billing_amount(Zone_xc, Type, WT):
    p1 = 'fwd' if Type=='Forward charges' else 'rto'
    p2 = Zone_xc
    fixed = Courier_Rates[p1+'_'+p2+'_'+'fixed']
    additional = (WT*2 - 1)*Courier_Rates[p1+'_'+p2+'_'+'additional']
    return fixed+additional


# In[112]:


Courier_Rates


# In[120]:


master_df['Expected Amount'] = master_df.apply(lambda row:get_billing_amount(row['Zone_xc'], row['Type of Shipment'], row['Slab WT']), axis=1)


# In[121]:


master_df[['Billing Amount (Rs.)', 'Expected Amount']]


# In[122]:


p_diff = sum(master_df['Billing Amount (Rs.)']> master_df['Expected Amount'])
n_diff = sum(master_df['Billing Amount (Rs.)']< master_df['Expected Amount'])
similar = sum(master_df['Billing Amount (Rs.)'] == master_df['Expected Amount'])


# In[123]:


p_diff,n_diff,similar


# In[ ]:




