setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(ggplot2)


# get nrms contrast accordingly
get_nrmscontrast<-function(dat)
{
  dat<-"sub1"
  datn <- paste(dat,".txt",sep="")

  
  # read data
  dt.df<-read.table(datn,header=TRUE)
  nrms.df<-read.table("nrmsContrast.csv",sep=",",header=TRUE)
  
  # add new columns
  dt.df$nrms<-NA
  dt.df$matched_nrms<-NA
  
  # search nrms contrast value according to tau, alpha, repeat
  for(i in 1:nrow(dt.df))
  {
    dt.df$nrms[i]<-nrms.df$nrmsConstrast[which(nrms.df$rep==dt.df$rep[i]
                                            &nrms.df$alpha==dt.df$a_test[i]
                                            &nrms.df$tau==dt.df$t_test[i])]
    dt.df$matched_nrms[i]<-nrms.df$nrmsConstrast[which(nrms.df$rep==dt.df$rep[i]
                                                    &nrms.df$alpha==dt.df$matched_alpha[i]
                                                    &nrms.df$tau==dt.df$t_test[i])] 
  }
  return(dt.df)
}

dat1<-"sub1"
dt <- get_nrmscontrast(dat1)
nrms <- dt[c(3,4,6,10)]
nrms.df <- subset(nrms, rep_id == 0) 
nrms.df$tau <- as.factor(nrms.df$t_test)

p1<- ggplot(nrms.df, aes(x=a_test, y=nrms, color=tau))+ 
  geom_point()+
  ylab("normalized rms contrast")+
  xlab("alpha")+
  theme_classic()+
  ggtitle("Normalized RMS Contrast") 
p1





