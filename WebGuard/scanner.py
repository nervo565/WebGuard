#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def check_sqli(url):
    """فحص ثغرات SQL Injection"""
    test_payloads = ["'", "\""]
    for payload in test_payloads:
        try:
            response = requests.get(f"{url}?id={payload}", timeout=5)
            if "sql" in response.text.lower() and "error" in response.text.lower():
                return True
        except:
            continue
    return False

def generate_report(results):
    """إنشاء تقرير مفصل"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("security_report.txt", "w") as f:
        f.write(f"📅 تاريخ التقرير: {timestamp}\n\n")
        for url, vulns in results.items():
            f.write(f"🔍 الموقع: {url}\n")
            if vulns:
                f.write("⚠️ الثغرات المكتشفة:\n")
                for vuln in vulns:
                    f.write(f"- {vuln}\n")
            else:
                f.write("✅ لا توجد ثغرات حرجة\n")
            f.write("\n" + "="*50 + "\n")

def main():
    print("""
    ██╗    ██╗███████╗██████╗  ██████╗ ██╗   ██╗
    ██║    ██║██╔════╝██╔══██╗██╔════╝ ██║   ██║
    ██║ █╗ ██║█████╗  ██████╔╝██║  ███╗██║   ██║
    ██║███╗██║██╔══╝  ██╔══██╗██║   ██║██║   ██║
    ╚███╔███╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝
     ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝ 
    """)
    
    try:
        with open("websites.txt", "r") as f:
            websites = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ ملف websites.txt غير موجود! يرجى إنشائه أولاً")
        return

    results = {}
    for site in websites:
        if not site.startswith(("http://", "https://")):
            site = "https://" + site
        
        print(f"\nجارٍ فحص: {site}")
        vulns = []
        
        if check_sqli(site):
            vulns.append("ثغرة SQL Injection")
        
        # يمكنك إضافة فحوصات أخرى هنا
        
        results[site] = vulns
    
    generate_report(results)
    print("\n✅ تم الانتهاء! التقرير جاهز في ملف security_report.txt")

if __name__ == "__main__":
    main()
