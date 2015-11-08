# Aggregate Data and analysis for Code Worker Quest
# Data Incubator Challenge
# Problem 3
library(data.table)
# Starting with 180 Countries and GPD growth data from Global Economic Prospects from The World Bank
hqdata <- as.data.frame(Data_Extract_From_Global_Economic_Prospects_Data[,c("Country.Name", "Country.Code")])
obs <- Data_Extract_From_Global_Economic_Prospects_Data[,c(5:15, 17:21)]
obs$X1999..1999. <- as.numeric(obs$X1999..1999.)
obs$X2000..2000. <- as.numeric(obs$X2000..2000.)
hqdata$"Obs.GDP.growth" <- rowMeans(obs, na.rm = T)
pred <- Data_Extract_From_Global_Economic_Prospects_Data[,c(22:23)]
hqdata$"Pro.GDP.growth" <- rowMeans(pred, na.rm = T)
hqdata.new <- hqdata[1:175,]
gallup <- as.data.table(gallup.median.income)
hqdata <- as.data.table(hqdata.new)
setnames(gallup, "V1", "Country.Name")
setkey(gallup$Country.Name)
setkey(hqdata$Country.Name)

join <- merge(gallup, hqdata, by="Country.Name", all=T)

digitalmathscores$S.E. <- NULL
digitalreadingscores$S.E. <- NULL
digitalmathscores <- as.data.table(digitalmathscores)
digitalreadingscores <- as.data.table(digitalreadingscores)
setnames(digitalmathscores, "Mean.score", "digi.math.score")
setnames(digitalreadingscores, "Mean.score", "digi.read.score")
setnames(digitalreadingscores, "Digital.reading.scale", "Country.name")
scores <- merge(digitalreadingscores, digitalmathscores, by="Country.name")
setnames(scores, "name", "Country.Name")
join$Country.Name <- as.character(join$Country.Name)
scores$name <- as.character(scores$name)
#scores$Country.Name <- NULL
scores$name <- gsub('Korea', 'South Korea', scores$name)
join$Country.Name <- gsub('Hong Kong', 'Hong Kong-China', join$Country.Name)
scores$Country.Name <- gsub('Slovak Republic', 'Slovakia', scores$Country.Name)



#scores$Country.Name <- lapply(tolower(scores$name), function(x) agrep(x, tolower(join$Country.Name), max.distance = 0.15, ignore.case = F, value = T))
setkey(scores, "Country.Name")
# lapply(tolower(datf1$name), function(x) agrep(x, tolower(datf2$name)))
join2 <- merge(join, scores, by="Country.Name", all=T)
setnames(join2, "V2", "gallup.median.income")

#write.csv(join2, "join2.csv", row.names=FALSE, na="")

pisa.summary <- as.data.frame(pisa.summary)
pisa.summary$Country.Name <- gsub('Korea', 'South Korea', pisa.summary$Country.Name)
pisa.summary$Country.Name <- gsub('Slovak Republic', 'Slovakia', pisa.summary$Country.Name)
pisa.summary$Country.Name <- gsub('Cyprus1, 2', 'Cyprus', pisa.summary$Country.Name)
pisa.summary$Country.Name <- gsub('Viet Nam', 'Vietnam', pisa.summary$Country.Name)

pisa.summary <- as.data.table(pisa.summary)
setkey(pisa.summary, "Country.Name")
join3 <- merge(join2, pisa.summary, by="Country.Name", all = T)

cypcitigroup.scores <- as.data.table(citigroup.scores)
largest.150.cities <- as.data.table(largest.150.cities)
cities <- merge(citigroup.scores, largest.150.cities, all.x = T, by="City.name")
top50citiespop <- as.data.table(top50citiespop)
setnames(top50citiespop, "V1", "City.name")
cities <- merge(cities, top50citiespop, all.x = T, by="City.name")
cities[,5:10] <- NULL
cities[,c(3,5,6)] <- NULL
list268cities <- as.data.table(list268cities)
setnames(list268cities, c("City", "Country"), c("City.name", "Country.name"))
cities <- merge(cities, list268cities, all.x = T, by=c("City.name", "Country.name"))
setnames(cities, "Country.name.x", "Country.name")

# write.csv(cities, "joinedcities.csv", row.names=FALSE, na="")
# write.csv(join3, "join3.csv", row.names=FALSE, na="")

setnames(joinedcities, "Country.name", "Country.Name")

joinedcities$Country.Name <- gsub("Egypt", "Egypt, Arab Rep.", joinedcities$Country.Name)
joinedcities$Country.Name[52] <- "Hong Kong-China"
joinedcities$Country.Name[104] <- "Shanghai-China"
total <- merge(join3, joinedcities, by = "Country.Name", all = T)
total[200, 2:5] <- total[42, 2:5]
total[101, 3:5] <- total[42, 3:5]
total[67,]
total <- total[-67,]
total[26,]
total <- total[-26,]

Code_Worker_Quest <- Code_Worker_Quest[,3:25]
Code_Worker_Quest <- as.data.table(Code_Worker_Quest)
pygal_world <- as.data.table(pygal_world)
setnames(pygal_world, "Country", "Country.Name")
setnames(pygal_world, "code", "pygal_code")



full_comb <- merge(Code_Worker_Quest, pygal_world, by = "Country.Name", all.x = T)

write.csv(full_comb, "Code_Worker_Quest.csv", row.names=FALSE, na="")

# FULL OUTER JOIN
# Result <- merge(Employees,Departments, all=TRUE)


# FULL OUTER JOIN WHERE NULL
# perform the join, retain only NA from matched cols on both side
#Result <- merge(Employees,Departments, all=TRUE)
#Result <- Result[is.na(EmployeeName) | is.na(DepartmentName)]