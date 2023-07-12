select count(*)as Broj,Tip_nekretnine as Tip_Nekretnine from nekretninepresiceno group by Tip_nekretnine

select Grad,count(*)as Broj from nekretninepresiceno group by Grad order by Broj desc

SELECT Tip_Nekretnine,Uknjizeno,count(*) as Broj FROM nekretninepresiceno group by Tip_Nekretnine,Uknjizeno order by Broj desc;

SELECT  * FROM nekretninepresiceno where Tip_nekretnine='Stanovi' order by Cena desc limit 30;

SELECT  * FROM nekretninepresiceno where Tip_nekretnine='Kuce' order by Cena desc limit 30;

SELECT  * FROM nekretnineprecisceno where Tip_nekretnine='Kuce' order by Kvadratura desc limit 100;
SELECT  * FROM nekretnineprecisceno where Tip_nekretnine='Stanovi' and Tip_ponude='Prodaja' order by Kvadratura desc limit 100;

SELECT * FROM nekretnineprecisceno where `Tip gradnje`='Novogradnja' and Tip_ponude='Izdavanje' order by Cena desc;
SELECT * FROM nekretnineprecisceno where `Tip gradnje`='Novogradnja' and Tip_ponude='Prodaja' order by Cena desc;


SELECT * FROM nekretnine.nekretnineprecisceno order by `Ukupan broj soba` Desc limit 30;
SELECT * FROM nekretnine.nekretnineprecisceno where Tip_nekretnine='Stanovi' order by Kvadratura Desc limit 30;
SELECT * FROM nekretnine.nekretnineprecisceno where Tip_nekretnine='Kuće' order by coalesce(`Površina placa`,0) desc;

SET SQL_SAFE_UPDATES = 0;
CREATE TABLE nekretnine_temp AS
SELECT MAX(idnekretnine) AS min_id
FROM nekretnine
  GROUP BY Tip_nekretnine, Cena, Kvadratura,Sprat,Spratnost,Uknjizeno,Grejanje,Namestenost,'Tip gradnje',Grad,'Deo grada','Broj kupatila';


DELETE  FROM nekretnine
WHERE idnekretnine NOT IN (
    SELECT min_id
    FROM nekretnine_temp
);
DROP TABLE nekretnine_temp;

