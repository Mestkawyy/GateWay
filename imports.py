def __init__(self, IEC104OR101=101, ip_104="", serialPort_101="" , baudrate_101=9600, sizeOfCA=0,sizeOfIOA=0, sizeOfCOT=0, originatorAddress=0, timeoutForAck=500,data_bits_length=8, parity_type='E', stop_bits_length=1, infinite_loop_trial=True, link_layer_mode=0,
log= None , datapoints = None,TempTodatapoints =None ,linked_layer_address = 1 , initial_value=-9999 , initial_timestamp=1 , _lock= None):

        global client
        
        self.autoUpdate=True
        self.initial_value = initial_value
        self.timestamp = initial_timestamp
        self.IEC104_or_101 = IEC104OR101
        self.infinite_loop_trial = infinite_loop_trial
        self.datapoints = {}
        self.TempTodatapoints = {}
        self.log = log
        # self.stop = False
        # self.lock = _lock
        
        """    for _, data_point in self.datapoints.items():
           print("data_point['recieved_mqtt']['GroupNO']") """

        if self.IEC104_or_101 == 101:
            # self.mqtt_client = mqtt_client

            self.serialPort = serialPort_101

            self.port = SerialPort_create(self.serialPort, baudrate_101, data_bits_length, ord(parity_type), stop_bits_length)

            self.slave = CS101_Slave_create(self.port , None , None , link_layer_mode)

            # self.rawMessageHandler = CS101_Master_setRawMessageHandler(self.raw_msg)
            
            self.alParameters = CS101_Slave_getAppLayerParameters(self.slave)
            
            setattr(self.alParameters,'sizeOfCA',sizeOfCA)
            setattr(self.alParameters,'sizeOfIOA',sizeOfIOA)
            setattr(self.alParameters,'sizeOfCOT',sizeOfCOT)
            setattr(self.alParameters,'originatorAddress',originatorAddress)

            print("SIZES OF PARAMETERS")
            print(sizeOfCOT)
            print(sizeOfIOA)
            print(originatorAddress)
            print(sizeOfCA)

            print('^^^^^')

            self.llParameters = CS101_Slave_getLinkLayerParameters(self.slave)
            self.clockSyncHandler = CS101_ClockSynchronizationHandler(self.clock)
            self.interrogationHandler = CS101_InterrogationHandler(self.General_interrogation)
            self.conterinterriogationHandler = CS101_CounterInterrogationHandler(self.Counter_interrogation)

            # self.interrogationHandler = CS101_InterrogationHandler(self.GI_h)
            self.asduHandler = CS101_ASDUHandler(self.ASDU_h)
            # change default application layer parameters (optional) 
            setattr(self.llParameters,'timeoutForAck',500)

            # # IEC60870_LINK_LAYER_UNBALANCED -> 1
            # # IEC60870_LINK_LAYER_BALANCED -> 0
            CS101_Slave_setLinkLayerAddress(self.slave , linked_layer_address)

            # CS101_Slave_setLinkLayerAddressOtherStation(self.slave, 2)

            CS101_Slave_setResetCUHandler(self.slave, CS101_ResetCUHandler(), None)

            CS101_Slave_setIdleTimeout(self.slave, 100000000)

            CS101_Slave_setLinkLayerStateChanged(self.slave , IEC60870_LinkLayerStateChangedHandler(), None)

            CS101_Slave_setInterrogationHandler(self.slave, self.interrogationHandler, None)

            CS101_Slave_setCounterInterrogationHandler(self.slave, self.conterinterriogationHandler, None)
            # CS101_Slave_setRawMessageHandler(self.slave , self.rawMessageHandler , None)

            CS101_Slave_setASDUHandler(self.slave, self.asduHandler, None)

            CS101_Slave_setClockSyncHandler(self.slave, self.clockSyncHandler, None)
            CS101_Slave_setResetCUHandler(self.slave, CS101_ResetCUHandler(), None)
            # CS101_Slave_setIdleTimeout(self.slave, 1500)
            CS101_Slave_setLinkLayerStateChanged(self.slave, IEC60870_LinkLayerStateChangedHandler(), None)
            CS101_Slave_setRawMessageHandler(self.slave, IEC60870_RawMessageHandler(), None)

            # # /* set the callback handler for the clock synchronization command */
            # CS104_Slave_setClockSyncHandler(self.slave, self.clockSyncHandler, None)

            # # /* set the callback handler for the interrogation command */
            # CS104_Slave_setInterrogationHandler(self.slave, self.interrogationHandler, None)

            # # /* set handler for other message types */
            # CS104_Slave_setASDUHandler(self.slave, self.asduHandler, None)

            # # /* set handler to handle connection requests (optional) */
            # CS104_Slave_setConnectionRequestHandler(self.slave, self.connectionRequestHandler, None)

            # # /* set handler to track connection events (optional) */
            # CS104_Slave_setConnectionEventHandler(self.slave, self.connectionEventHandler, None)

            # self.clockSyncHandler = CS101_ClockSynchronizationHandler(self.clock)
            # self.interrogationHandler = CS101_InterrogationHandler(self.General_interrogation)
            # self.asduHandler = CS101_ASDUHandler(self.ASDU_h)

            # self.serialPort = serialPort_101
            # self.port = SerialPort_create(serialPort_101, baudrate_101, data_bits_length, ord(parity_type),
            #                               stop_bits_length)


            # self.slave = CS101_Slave_create(self.port, None, None, link_layer_mode)

            # CS101_Slave_setLinkLayerAddress(self.slave, 1)
            # CS101_Slave_setLinkLayerAddressOtherStation(self.slave, 2)
            # self.alParams = CS101_Slave_getAppLayerParameters(self.slave)

            # setattr(self.alParams, 'sizeOfCA', sizeOfCA)
            # setattr(self.alParams, 'sizeOfIOA', sizeOfIOA)
            # setattr(self.alParams, 'sizeOfCOT', sizeOfCOT)
            # setattr(self.alParams, 'originatorAddress', originatorAddress)

            # self.llParameters = CS101_Slave_getLinkLayerParameters(self.slave)
            # setattr(self.llParameters, 'timeoutForAck', timeoutForAck)

            # CS101_Slave_setClockSyncHandler(self.slave, self.clockSyncHandler, None)
            # CS101_Slave_setASDUHandler(self.slave, self.asduHandler, None)
            # CS101_Slave_setResetCUHandler(self.slave, CS101_ResetCUHandler(), None)
            # CS101_Slave_setIdleTimeout(self.slave, 1500)
            # CS101_Slave_setLinkLayerStateChanged(self.slave, IEC60870_LinkLayerStateChangedHandler(), None)
            # CS101_Slave_setRawMessageHandler(self.slave, IEC60870_RawMessageHandler(), None)

            if SerialPort_open(self.port):
                print()
                # instances_101+=1
                # print(f"Port {serialPort_101} opened successfully !")
                print(f"Port of the IEC60870-5-101 for instance number= {serialPort_101}")
                print("An IEC60870-5-101 slave instance has been started successfully !")
                print()
            else:
                print(f"Port {serialPort_101} failed to start , Bye !")
                raise ConnectionError("Connection failed due to something made wrong")
                exit(0)

        elif self.IEC104_or_101 == 104:
            print("104 CONNECTED.......")

            self.ip_104 = ip_104
            self.clockSyncHandler = CS101_ClockSynchronizationHandler(self.clock)
            self.interrogationHandler = CS101_InterrogationHandler(self.General_interrogation)
            # self.interrogationHandler = CS101_InterrogationHandler(self.GI_h)
            self.asduHandler = CS101_ASDUHandler(self.ASDU_h)

            self.connectionRequestHandler = CS104_ConnectionRequestHandler(self.Conn_req)
            self.connectionEventHandler = CS104_ConnectionEventHandler(self.Conn_event)
            self.slave = CS104_Slave_create(100, 100)
            CS104_Slave_setLocalAddress(self.slave, ip_104)

            #   /* Set mode to a single redundancy group
            CS104_Slave_setServerMode(self.slave, CS104_MODE_SINGLE_REDUNDANCY_GROUP)

            # /* get the connection parameters - we need them to create correct ASDUs */
            self.alParams = CS104_Slave_getAppLayerParameters(self.slave)
            self.alParameters = CS104_Slave_getAppLayerParameters(self.slave)

            setattr(self.alParams, 'sizeOfCA', sizeOfCA)
            setattr(self.alParams, 'sizeOfIOA', sizeOfIOA)
            setattr(self.alParams, 'sizeOfCOT', sizeOfCOT)
            # setattr(self.alParams,'originatorAddress',originatorAddress)

            # /* set the callback handler for the clock synchronization command */
            CS104_Slave_setClockSyncHandler(self.slave, self.clockSyncHandler, None)

            # /* set the callback handler for the interrogation command */
            CS104_Slave_setInterrogationHandler(self.slave, self.interrogationHandler, None)

            # /* set handler for other message types */
            CS104_Slave_setASDUHandler(self.slave, self.asduHandler, None)

            # /* set handler to handle connection requests (optional) */
            CS104_Slave_setConnectionRequestHandler(self.slave, self.connectionRequestHandler, None)

            # /* set handler to track connection events (optional) */
            CS104_Slave_setConnectionEventHandler(self.slave, self.connectionEventHandler, None)
            print()
            # instances_104+=1
            print("An IEC60870-5-104 slave instance has been started successfully !")
            print(f"IP of the IEC60870-5-104 for = {ip_104}")
            print()

        else:
            print("Wrong protocol has been specified , try to enter a valid number to be 101 or 104")

    def updates(self,typeId,ioa,asdu_no,value,ts,is_101) :
        print("updates")
        originator_address=0
        ASDU=CS101_ASDU_create(self.alParameters, False, CS101_COT_SPONTANEOUS, originator_address , asdu_no, False, False)
        #ASDU_1=CS101_ASDU_create(self.alParameters, False, CS101_COT_PERIODIC, originator_address , asdu_no, False, False)
        #ASDU_2=CS101_ASDU_create(self.alParameters, False, CS101_COT_BACKGROUND_SCAN, originator_address , asdu_no, False, False)
        

        type_without_time = [1, 3, 5, 9, 11,13,15,45,100]  # these type_identification that indicates that this type is not with time stamp
        type_with_time = [2,4,6,10,14,16,30,31,32,34,35,36,37]  # these type_identification that indicates that this type is not with time stamp
        if typeId in type_without_time :
            #
            io2 = self.create_data_object_without_time(typeId, value, ioa, initial_value = 4444)
            CS101_ASDU_addInformationObject(ASDU , io2)
            #CS101_ASDU_addInformationObject(ASDU_1 , io2)
           # CS101_ASDU_addInformationObject(ASDU_2 , io2)


            print("io",io2)
            #ioa11=InformationObject_getObjectAddress(cast(io22,InformationObject))
            #print("ioa",ioa11)
            InformationObject_destroy(io2)
        else :
            io2 = self.create_data_object_with_time(typeId, value, ioa,  CPTime2a=ts,initial_value = 4444)
            CS101_ASDU_addInformationObject(ASDU , io2)
            InformationObject_destroy(io2)


        if is_101==1:
            print("is_101 true")
            CS101_Slave_enqueueUserDataClass2(self.slave,ASDU)
            

        else:
            CS104_Slave_enqueueASDU(self.slave,ASDU)
            print("is_101 false")
