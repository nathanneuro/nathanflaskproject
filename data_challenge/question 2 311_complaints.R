# 311 Service Requests from 2010 to Present
# Data Challenge Question 2
library(data.table)
# Part 1
# What fraction of complaints are associated with 2nd most poppular agency?
# Select Agency column
# Determine second most common
# Count of second most common / total
options(digits=10)
agency <- `311_Service_Requests_from_2010_to_Present`$Agency
summary(agency)
afreq <- ftable(agency)
afreq
aprop = sort(prop.table(afreq), decreasing = T)
aprop[2]

# Part 2
# Most surprising complaint type conditioned on Borough
# Surprise = cond prob given bur / uncond prob of complaint type

type = data.frame(`311_Service_Requests_from_2010_to_Present`$Complaint.Type, `311_Service_Requests_from_2010_to_Present`$Borough)
summary(type)
names(type) <- c("Complaint.Type", "Borough")
type <- data.table(type)
setkey(type, Borough)
summarise(type)
type$Borough[which(type$Borough== "")] <- "Unspecified"
type <- type[type$Borough != "Unspecified",]
# Instructions: Average ability by grade
# stulevel_agg_4 <- as.data.frame(stulevel[, j=list(mean(ability, na.rm = TRUE),mean(attday, na.rm = TRUE)),by = list(year,grade)])


#condprobtable - actually a set of tables, one for each burough
counttable <- as.data.frame(table(type$Complaint.Type, type$Borough))
counttable <- data.table(counttable)
setkey(counttable, Var2)
## Convert df into a data.table
#dt <- data.table(df) 
## Set Year as a key
#setkey(dt, "Year") 
## Calculate the sum of sales per year(=key(dt))
#X <- dt[, list(SUM=sum(Sales)), by=key(dt)] 
## Join X and dt, both have the same key and
## add the share of sales as an additional column
#R3 <- dt[X, list(Sales, Product, Share=Sales/SUM)]
#head(R3)
X <- counttable[, list(SUM=sum(Freq)), by=key(counttable)]

R3 <- counttable[X, list(Var1, Var2, CP=Freq/SUM)]

# should be count of complaint type / total number of complaints
Y <- as.data.frame(prop.table(table(type$Complaint.Type)))
Y <- data.table(Y)

sum(Y$Freq)
sum(R3$CP, na.rm = TRUE)
sum(R3$CP[which(R3$Var2 == "BRONX")], na.rm = T)

setkey(Y, Var1)
setkey(R3, Var1)
Z <- merge(R3, Y, all.x = TRUE)

Z <- Z[, list(Var1, Var2, CP, Freq, Surprise= CP / Freq)]
setorder(Z, -Surprise, na.last = TRUE)
head(Z)

# Part 3
latitude <- `311_Service_Requests_from_2010_to_Present`$Latitude
q <- quantile(latitude, probs = c(.1, .9), na.rm = T)
q[2]-q[1]
#quantile(x, probs = c(0, 0.25, 0.5, 0.75, 1)) 

# Part 4
squaredegree = 12365.1613 # square kilometers
longitude <- (`311_Service_Requests_from_2010_to_Present`$Longitude)
longi <- summary(longitude)
lati <- summary(latitude)
ellipsearea = pi * sd(latitude, na.rm = T) * sd(longitude, na.rm = T) * squaredegree
ellipsearea

# Part 5
datetime <- as.data.frame(`311_Service_Requests_from_2010_to_Present`$Created.Date)
library(chron)
names(datetime) <- c("string")
as.character(datetime$string)
dtparts <- as.data.frame(strptime(as.character(datetime$string), "%m/%d/%Y %I:%M:%S %p"))
names(dtparts) <- c("conv")
hours = times(strftime(dtparts$conv, format="%T"))
hours <- as.data.frame(hours)
hours$numb <- hours(hours$hours)
htable <- table(hours$numb)
phtable <- prop.table(htable)
sort(htable, decreasing = T)
sort(phtable, decreasing = T)
htable[12]-htable[5]
8802-818

# Part 6
# time between calls in seconds
timediff <- as.numeric(diff(dtparts$conv))
sd(timediff)






