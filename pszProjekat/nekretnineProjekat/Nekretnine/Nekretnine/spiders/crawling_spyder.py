import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
    file= '../../output.json'
    open(file, 'w').close()
    name = "nekretninecrawler"
    #allowed_domains = "sasomange.rs"
    start_urls=[
        # 'https://sasomange.rs/h/sve-nekretnine',
        # 'https://sasomange.rs/c/kuce-prodaja/f/beograd?currentPage=1'
              'https://sasomange.rs/c/stanovi-prodaja/f/beograd?currentPage=1',
              # 'https://sasomange.rs/c/stanovi-iznajmljivanje/f/beograd-palilula?currentPage=1',
            #    'https://sasomange.rs/c/kuce-iznajmljivanje/f/?currentPage=1',
    ]
    rules = (
        Rule(LinkExtractor(allow="sasomange.rs/p/"), callback="parse_item"),
      # Rule(LinkExtractor(allow="sasomange.rs/c/stanovi-iznajmljivanje/"),callback="parse_item2"),
        Rule(LinkExtractor(allow="sasomange.rs/c/stanovi-prodaja"),callback="parse_item2"),

        #Kuceee
     #  Rule(LinkExtractor(allow="sasomange.rs/c/kuce-iznajmljivanje"), callback="parse_item2"),
       #Rule(LinkExtractor(allow="sasomange.rs/c/kuce-prodaja"),callback="parse_item2"),

        #Stanovii
        #Rule(LinkExtractor(allow="sasomange.rs/f/")),
        #Rule(LinkExtractor(allow="sasomange.rs/h/svenekretnine")),


    )
    # def start_requests(self):
    #     yield scrapy.Request('https://www.halooglasi.com/nekretnine/', meta={'playwright': True})
    def parse_item(self, response):
        #if (response.css('.js-pdp-breadcrumb-item::text')[3].get()=='Stanovi'):
            if  len(response.xpath('//span[@class="price-content"]/text()'))!=0:
         #    if (response.css('.js-pdp-breadcrumb-item::text')[2].get()=='Prodaja'):
                yield{
                    'Tip_ponude':response.css('.js-pdp-breadcrumb-item::text')[2].get(),
                    'Tip_nekretnine':response.css('.js-pdp-breadcrumb-item::text')[3].get(),
                    'Broj soba':response.xpath("//p[text()[contains(.,'Broj soba')]]/..//span/text()").get(),
                    'Cena':''.join(filter(str.isdigit,response.xpath('//span[@class="price-content"]/text()').get('\\').split()[0])) if len(response.xpath('//span[@class="price-content"]'))>0 else None,
                    'Cena_kvadrat': response.xpath('//span[@class="alternative-price"]/text()').get('\\').split()[0] if  response.xpath('//span[@class="alternative-price"]/text()').get('\\')!='\\' else None,
                    'Kvadratura':response.xpath("//p[text()[contains(.,'Površina')]]/..//span/text()").get(),
                    'Sprat':response.xpath("//p[text()[contains(.,'Sprat')]]/..//span/text()").get(),
                    'Spratnost': response.xpath("//p[text()[contains(.,'spratnost')]]/..//span/text()").get(),
                    'Uknjizeno':response.xpath("//p[text()[contains(.,'Uknjiženo')]]/..//span/text()").get() !=None,
                    'Grejanje': response.xpath("//p[text()[contains(.,'Grejanje')]]/..//span/text()").get(),
                    "Ukupan broj soba":response.xpath("//p[text()[contains(.,'Struktura')]]/..//span/text()").get(),
                    "Namestenost":response.xpath("//p[text()[contains(.,'Nameštenost')]]/..//span/text()").get(),
                    "Broj kupatila":''.join(filter(str.isdigit,response.xpath("//p[text()[contains(.,'Broj kupatila')]]/..//span/text()").get())) if len(response.xpath("//p[text()[contains(.,'Broj kupatila')]]/..//span"))!=0 else None,
                    "Tip gradnje":response.xpath("//p[text()[contains(.,'Tip gradnje')]]/..//span/text()").get(),
                    "Stanje objekta":response.xpath("//p[text()[contains(.,'Stanje objekta')]]/..//span/text()").get(),
                    "Grad":response.css('.js-pdp-breadcrumb-item::text')[4].get().split('/')[0] if len(response.css('.js-pdp-breadcrumb-item::text'))>=4  else None,
                    "Deo grada":response.css('.js-pdp-breadcrumb-item::text')[4].get().split('/')[1] if len(response.css('.js-pdp-breadcrumb-item::text'))>=4 and len(response.css('.js-pdp-breadcrumb-item::text')[4].get().split('/'))>1  else None ,
                    "MikroLokacija": response.css('.js-pdp-breadcrumb-item::text')[4].get().split('/')[2] if len( response.css('.js-pdp-breadcrumb-item::text')) >= 4 and len(response.css('.js-pdp-breadcrumb-item::text')[4].get().split('/')) > 2 else None,
                    "Površina placa":response.xpath("//p[text()[contains(.,'Površina placa')]]/..//span/text()").get(),
                    "Parking": len(response.xpath("//p[text()[contains(.,'Parking')]]/..//img")) != 0,
                    "Lift": len(response.xpath("//p[text()[contains(.,'Lift')]]/..//img")) != 0,
                    "Link":  str(response).split(' ')[1].split('>')[0]

        }

    def parse_item2(self, response):
     #   print(response)
        responseParts= str(response).split(' ')
        status=responseParts[0].split('<')[1]
        print(responseParts[1])
        if (status=='200'):
            for product in response.xpath('//a[@class="product-link"]/@href'):
                #print ('https://sasomange.rs/'+product.get())
                yield response.follow('https://sasomange.rs/'+product.get(),callback=self.parse_item)
            if len(response.xpath('//a[@class="product-link"]/@href'))>10:

                responseTxt = responseParts[1].split('>')[0]
               # print (responseTxt)
                if '?' in responseTxt:
                    parts=responseTxt.split('currentPage=')
                    nextpage = parts[0]+'currentPage='+str(int(parts[1])+1)
                else:
                    nextpage=responseTxt+'?currentPage=1'
                #print(nextpage)
                if (nextpage is not None):
                    yield response.follow(nextpage, callback=self.parse_item2)
#    def parse_item(self, response):
# – tip nekretnine
# (stan ili kuća), tip ponude (prodaja ili iznajmljivanje), lokacija - grad i deo grada gde se lokacija nalazi,
# kvadratura nekretnine, godina izgradnje (ukoliko postoji), površina zemljišta (samo za kuće), spratnost
# (ukupna i sprat na kojoj se nalazi, samo za stanove), uknjiženost (da/ne), tip grejanja, ukupan broj
# soba, ukupan broj kupatila (toaleta), podaci o parkingu (da/ne) i ostale dodatne informacije (da li ima
# lift u zgradi, da li ima terasu/lođu/balkon).