class Datasource:
    def __init__(self, datasource_name, datasource_source):
        self.datasource_UID = None
        self.datasource_name = datasource_name
        self.datasource_source = datasource_source
    
    def __eq__(self, other):
        return self.datasource_name == other.datasource_name and self.datasource_source == other.datasource_source
    
class Datasources:
    def __init__(self):
        self.datasources = []
        self.num_of_datasources = 0

    def add(self, datasource):
        found = False

        if self.num_of_datasources == 0:
            self.datasources.append(datasource)
            self.num_of_datasources += 1
            print("A new datasource has been added: {}.".format(datasource.datasource_name))
            return self.datasources[-1]
        else:
            for i in range(self.num_of_datasources):
                if datasource == self.datasources[i]:
                    found = True
                    print("This datasource has already been added: {}.".format(datasource.datasource_name))
                    return self.datasources[i]
            
            if not found:
                self.datasources.append(datasource)
                self.num_of_datasources += 1
                print("A new datasource has been added: {}.".format(datasource.datasource_name))
                return self.datasources[-1]

class Dataset:
    def __init__(self, dataset_name, datasource_uid):
        self.dataset_uid = None
        self.dataset_name = dataset_name
        self.datasource_uid = datasource_uid
    
    def __eq__(self, other):
        return self.dataset_name == other.dataset_name and self.datasource_uid == other.datasource_uid

class Datasets:
    def __init__(self):
        self.datasets = []
        self.num_of_datasets = 0
    
    def add(self, dataset):
        found = False
        
        if self.num_of_datasets == 0:
            self.datasets.append(dataset)
            self.num_of_datasets += 1
            print("A new dataset has been added: {}.".format(dataset.dataset_name))
            return self.datasets[-1]
        else:
            for i in range(self.num_of_datasets):
                if dataset == self.datasets[i]:
                    found = True
                    print("This dataset has already been added: {}.".format(dataset.dataset_name))
                    return self.datasets[i]
            
            if not found:
                self.datasets.append(dataset)
                self.num_of_datasets += 1
                print("A new dataset has been added: {}.".format(dataset.dataset_name))
                return self.datasets[-1]

class Datafile:
    def __init__(self, datafile_name, import_timestamp, dataset_uid):
        self.import_uid = None
        self.datafile_name = datafile_name
        self.import_timestamp = import_timestamp
        self.dataset_uid = dataset_uid
    
    def __eq__(self, other):
        return self.datafile_name == other.datafile_name and self.import_timestamp == other.import_timestamp and self.dataset_uid == other.dataset_uid

class Datafiles:
    def __init__(self):
        self.datafiles = []
        self.num_of_datafiles = 0
    
    def add(self, datafile):
        found = False
        
        if self.num_of_datafiles == 0:
            self.datafiles.append(datafile)
            self.num_of_datafiles += 1
            print("A new datafile has been added: {}.".format(datafile.datafile_name))
            return self.datafiles[-1]
        else:
            for i in range(self.num_of_datafiles):
                if datafile == self.datafiles[i]:
                    found = True
                    print("This datafile has already been added: {}.".format(datafile.datafile_name))
                    return self.datafiles[i]
            
            if not found:
                self.datafiles.append(datafile)
                self.num_of_datafiles += 1
                print("A new datafile has been added: {}.".format(datafile.datafile_name))
                return self.datafiles[-1]

class DatafileController:
    def __init__(self):
        pass

    def create_imp_datafile_with_mapping(self, mapping):
        datasources = Datasources()
        datasets = Datasets()
        datafiles = Datafiles()

        for sources in range(len(mapping["Datasources"])):
            datasource_name = mapping["Datasources"][sources]["Datsource_Name"]
            datasource_source = mapping["Datasources"][sources]["Datsource_Source"]
            datasource = datasources.add(Datasource(datasource_name, datasource_source))

            for sets in range(len(mapping["Datasources"][sources]["Datasets"])):
                dataset_name = mapping["Datasources"][sources]["Datasets"][sets]["Dataset"]
                dataset = datasets.add(Dataset(dataset_name, datasource))

                for files in range(len(mapping["Datasources"][sources]["Datasets"][sets]["Datafiles"])):
                    datafile_name = mapping["Datasources"][sources]["Datasets"][sets]["Datafiles"][files]["Datafile_Name"]
                    import_timestamp = mapping["Datasources"][sources]["Datasets"][sets]["Datafiles"][files]["Import_Timestamp"]
                    datafiles.add(Datafile(datafile_name, import_timestamp, dataset))

        return datasources, datasets, datafiles