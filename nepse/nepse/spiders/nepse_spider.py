import scrapy
from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

class NepseSpider(scrapy.Spider):
	name = "nepse"
	start_urls = ["http://merolagani.com/CompanyList.aspx"]

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self,response):
		accord = response.css("div#accordion")
		# extract the name of listed companies
		for panel in accord:
			for pl in panel.css("div.panel-group"):
				listed_companies = pl.css("div.panel div.panel-heading h3 a::text").extract()

		# get URL of all listed companies
		company_by_url = {}
		for panel in accord:
			for pl in panel.css("div.panel-group"):
				i=0
				for p in pl.css("div.panel"):
					company_by_url[listed_companies[i]]= p.css("table.table tr td a::attr(href)").extract()
					i = i+1
		# get current valuation of company 
		company_current_value = {}
		for panel in accord:
			for pl in panel.css("div.panel-group"):
				i=0
				for p in pl.css("div.panel"):
					company_current_value[listed_companies[i]]= p.css("table.table tr td a::attr(href)").extract()
					i = i+1

		# Choose first company listed under Commercial Section and extract the historical data:
		# up to page 16 : 2011/12/27
		xpaths = [
					'//*[@id="tabs"]/ul/li[4]/a',
					'//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[1]/div[2]/a[4]',
					'//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[1]/div[2]/a[4]',
					'//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[1]/div[2]/a[5]',
					'//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[1]/div[2]/a[6]',
					'//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[1]/div[2]/a[7]',
					'//*[@id="ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice"]/div[1]/div[2]/a[8]',




		]
		# print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		# print company_by_url[listed_companies[0]]
		# print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'



		# print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
		# print company_by_url[listed_companies[0]][0].split("=")[1]
		# print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

		self.driver.get("http://merolagani.com"+company_by_url[listed_companies[0]][0])
		
		
		history_data = []
		try:
			for xpath in xpaths:
				button = self.driver.find_element_by_xpath(xpath)
				button.click()
				element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice")))
				if element:
					xpath_response = Selector(text=self.driver.page_source)
					res = xpath_response.css("div#ctl00_ContentPlaceHolder1_CompanyDetail1_divDataPrice")
					for tab in res.css("div.table-responsive"):
						for t in tab.css("table.table tr"):
							# print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
							# print t.css("td::text").extract()
							history_data.append(t.css("td::text").extract())
		except Exception as e:
			print "Something is Wrong.........\n"
			print e

		finally:
			self.driver.quit()

		company_name = company_by_url[listed_companies[0]][0].split("=")[1]
		file_name = company_name+".csv"

		with open(file_name,'w') as file:
			writer=csv.writer(file)
			writer.writerow(["SNo.","Date", "LTP", "%Change", "High", "Low", "Open", "Qty","Turnover"])
			for row in history_data:
				writer.writerow(row)








