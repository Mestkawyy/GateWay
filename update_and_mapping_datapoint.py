   def dataPointUpdate(self) :
      

        #
        onceSended=0
        times=0
        for (data_pointKey, data_point) ,(Tempdata_pointKey, Tempdata_point) in zip( self.datapoints.items(),self.TempTodatapoints.items() ):
            # originator_address to correct
            times = times +1
            print(times)
            originator_address=0
            ASDU_number = data_point['asdu']
            ASDU=CS101_ASDU_create(self.alParameters, False, CS101_COT_SPONTANEOUS, originator_address , ASDU_number, False, False)
            #ASDU_1=CS101_ASDU_create(self.alParameters, False, CS101_COT_PERIODIC, originator_address , ASDU_number, False, False)
           # ASDU_2=CS101_ASDU_create(self.alParameters, False, CS101_COT_BACKGROUND_SCAN, originator_address , ASDU_number, False, False)


            type_without_time = [1, 3, 5, 9, 13, 15]  # these type_identification that indicates that this type is not with time stamp
            type_with_time = [2,4,6,10,14,16,30,31,32,34,35,36,37]  # these type_identification that indicates that this type is not with time stamp
           
            print(data_point['recieved_mqtt']['value'] )
            if data_point['recieved_mqtt']['value'] == Tempdata_point['recieved_mqtt']['value'] :

               #
                self.TempTodatapoints[Tempdata_pointKey]['recieved_mqtt']['value']=\
                    self.datapoints[data_pointKey]['recieved_mqtt']['value']
                if data_point['typeId'] in type_without_time :
                    #
                    onceSended = onceSended + 1
                    io2 = self.create_data_object_without_time(data_point['typeId'], data_point['recieved_mqtt']['value'], data_point['ioa'], initial_value = 4444)
                    CS101_ASDU_addInformationObject(ASDU , io2)
                   # CS101_ASDU_addInformationObject(ASDU_1 , io2)
                   # CS101_ASDU_addInformationObject(ASDU_2 , io2)
                    InformationObject_destroy(io2)
                    CS101_Slave_enqueueUserDataClass2(self.slave,ASDU)
                    print("GI_typeId")
                    print(data_point['typeId'])
                    print("ioa")
                    print(data_point['ioa'])
                    print("data_point")
                    print(data_point['recieved_mqtt']['value'])
                    print("Tempdata_point")
                    print(Tempdata_point['recieved_mqtt']['value'])
                else :
                    io2 = self.create_data_object_without_time(data_point['typeId'], data_point['recieved_mqtt']['value'], data_point['ioa'], initial_value = 4444)
                    CS101_ASDU_addInformationObject(ASDU , io2)
                    InformationObject_destroy(io2)
                    CS101_Slave_enqueueUserDataClass2(self.slave,ASDU)
                    print("boooom")

    def double_point_value_mapping(self, value):
        if value == 0:
            return IEC60870_DOUBLE_POINT_INTERMEDIATE
        elif value == 1:
            return IEC60870_DOUBLE_POINT_OFF
        elif value == 2:
            return IEC60870_DOUBLE_POINT_ON
        elif value == 3:
            return IEC60870_DOUBLE_POINT_INDETERMINATE
        else:
            return IEC60870_DOUBLE_POINT_INDETERMINATE

    def printCP56Time2a(self, time):

        print("%02i:%02i:%02i %02i/%02i/%04i" % (CP56Time2a_getHour(time),
                                                 CP56Time2a_getMinute(time),
                                                 CP56Time2a_getSecond(time),
                                                 CP56Time2a_getDayOfMonth(time),
                                                 CP56Time2a_getMonth(time),
                                                 CP56Time2a_getYear(time) + 2000))

