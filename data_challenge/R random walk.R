# https://stat.ethz.ch/pipermail/r-help/2010-December/261947.html

# compute path
n <- 10000
rw <- matrix(0, ncol = 2, nrow = n)
# generate the indices to set the deltas
indx <- cbind(seq(n), sample(c(1, 2), n, TRUE))

# now set the values
rw[indx] <- sample(c(-1, 1), n, TRUE)
# cumsum the columns
rw[,1] <- cumsum(rw[, 1])
rw[, 2] <- cumsum(rw[, 2])

plot(0,type="n",xlab="x",ylab="y",main="Random Walk Simulation
     In Two Dimensions",col=1:10,xlim=range(rw[,1]),ylim=range(rw[,2]))

# use 'segments' to color each path
segments(head(rw[, 1], -1)
         , head(rw[, 2], -1)
         , tail(rw[, 1], -1)
         , tail(rw[, 2], -1)
         , col = rainbow(nrow(rw) -1)  # a range of colors
)

end<-cbind(rw[10000,1],rw[10000,2])
start<-cbind(0,0)

points(start,pch=16,col="green", cex = 3)
points(end,pch=16,col="red", cex = 3)