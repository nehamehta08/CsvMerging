from datetime import date
import glob
import os
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings


def upload_view(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file_upload')
        merged_df = pd.DataFrame()
        
        for file in uploaded_files:
            df = pd.read_csv(file)
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        
        # Save merged DataFrame to a temporary CSV file
        filename = "merged_file_"+ str(date.today()) + ".csv"
        merged_file_path = os.path.join(settings.MEDIA_ROOT, filename)
        merged_df.to_csv(merged_file_path, index=False)
        return render(request, 'download_merged_file.html')
    
    return render(request, 'upload_files.html')


def download_view(request):
    
    media_dir = settings.MEDIA_ROOT
    file_list = glob.glob(os.path.join(media_dir, '*.csv'))
    print(file_list)
    if file_list:
        latest_file = max(file_list, key=os.path.getmtime)
        with open(latest_file, 'rb') as file:
            file_content = file.read()
        response = HttpResponse(file_content, content_type='text/csv')
        filename = os.path.basename(latest_file)
        response['Content-Disposition'] = f'attachment; filename={filename}'
        os.remove(latest_file)
        return response
    else:
        # Handle the case when no CSV files are found
        return HttpResponse("No CSV files found")

