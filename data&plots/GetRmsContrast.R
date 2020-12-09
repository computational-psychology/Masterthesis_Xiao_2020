setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
library(ggplot2)


# get RMS contrast accordingly
get_RMScontrast<-function(dat)
{
  dat<-"sub1"
  datn <- paste(dat,".txt",sep="")

  
  # read data
  dt.df<-read.table(datn,header=TRUE)
  rms.df<-read.table("rmsContrast.csv",sep=",",header=TRUE)
  
  # add new columns
  dt.df$rms<-NA
  dt.df$matched_rms<-NA
  
  # search rms contrast value according to tau, alpha, repeat
  for(i in 1:nrow(dt.df))
  {
    dt.df$rms[i]<-rms.df$rmsConstrast[which(rms.df$rep==dt.df$rep[i]
                                            &rms.df$alpha==dt.df$a_test[i]
                                            &rms.df$tau==dt.df$t_test[i])]
    dt.df$matched_rms[i]<-rms.df$rmsConstrast[which(rms.df$rep==dt.df$rep[i]
                                                    &rms.df$alpha==dt.df$matched_alpha[i]
                                                    &rms.df$tau==dt.df$t_test[i])] 
  }
  return(dt.df)
}

dat1<-"sub1"
dt <- get_RMScontrast(dat1)
rms <- dt[c(3,4,6,10)]
rms.df <- subset(rms, rep_id == 0) 
rms.df$tau <- as.factor(rms.df$t_test)

p1<- ggplot(rms.df, aes(x=a_test, y=rms, color=tau))+ 
  geom_point(alpha = 0.5)+
  ylab("rms contrast")+
  xlab("alpha")+
  theme_classic()+
  ggtitle("Rms Contrast") 
p1





