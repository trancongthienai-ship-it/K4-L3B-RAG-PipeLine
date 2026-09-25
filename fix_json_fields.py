import json
import os

file_path = "data/landing/news/summary.jsonl"
fixed_lines = []

try:
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            
            data = json.loads(line)
            
            # Đổi tên trường crawled_at -> date_crawled
            if 'crawled_at' in data:
                data['date_crawled'] = data.pop('crawled_at')
            
            # Đổi tên trường content -> content_markdown
            if 'content' in data:
                data['content_markdown'] = data.pop('content')
                
            fixed_lines.append(json.dumps(data, ensure_ascii=False))

    # Ghi đè lại file cũ với các trường đã được sửa
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in fixed_lines:
            f.write(line + '\n')
            
    print(f"Đã sửa thành công {len(fixed_lines)} dòng trong {file_path}")
    
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")
