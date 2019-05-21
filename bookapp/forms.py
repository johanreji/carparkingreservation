

from django import forms
from datetime import datetime, timedelta

class BookingSearchForm(forms.Form):
	startdate = forms.DateField(label="Start Date : ")
	starttime = forms.TimeField(label="Start Time : ")
	enddate = forms.DateField(label="End Date : ")
	endtime = forms.TimeField(label="End Time : ")
	curr_datetime=datetime.now()
	def clean(self):
		cleaned_data=super().clean()
		start_date=cleaned_data.get("startdate")
		end_date=cleaned_data.get("enddate")
		start_time=cleaned_data.get("starttime")
		end_time=cleaned_data.get("endtime")
		start_datetime=datetime.combine(start_date, start_time)
		end_datetime=datetime.combine(end_date, end_time)
		duration=end_datetime-start_datetime
		duration_min=divmod(duration.total_seconds(),60)[0]  
		if(start_datetime>end_datetime):
			raise forms.ValidationError(
                    "start date and time must be less than end date and time"
                )
		if(duration_min<=5):
			raise forms.ValidationError(
                    "minimum booking time is 5 min"
                )
		if(start_datetime<(self.curr_datetime-timedelta(minutes=5))):
			raise forms.ValidationError(
                    "start time should be greater than current time"
                )	
		self.cleaned_data.update(startdatetime=start_datetime)
		self.cleaned_data.update(enddatetime=end_datetime)

