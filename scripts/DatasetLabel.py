class DatasetLabel:

    dataset_labels = {
        'Child' : 0,
        'Elderly' : 1,
        'Adult' : 2,
        'Wheelchair' : 3,
        'Blind' : 4,
        'Suitcase' : 5,
        'Stroller' : 6,
        'Bicycle' : 7,
        'Scooter' : 8
    }
    
    def __init__(self, dataset_version_path: str):
        self.dataset_version = dataset_version_path
    
    def get_valid_id_class(self, dataset_sub, current_id):
        if 'dataset_1' in self.dataset_version:
            if dataset_sub != 'Stroller':
                if dataset_sub == 'Child_Elderly_Adult':
                    return current_id
                else:
                    return self.dataset_labels[dataset_sub]
            else:
                if current_id == '1':
                    return self.dataset_labels['Wheelchair']
                elif current_id == '2':
                    return self.dataset_labels['Suitcase']
                elif current_id == '3':
                    return self.dataset_labels['Stroller']
                elif current_id == '4':
                    return self.dataset_labels['Bicycle']
        elif 'dataset_2' in self.dataset_version:
            if dataset_sub == 'On_the_road':
                if current_id == '6':
                    return self.dataset_labels['Bicycle']
                elif current_id == '10':
                    return self.dataset_labels['Blind']
                elif current_id == '11':
                    return self.dataset_labels['Blind']
                elif current_id == '13':
                    return self.dataset_labels['Wheelchair']
                elif current_id == '14':
                    return self.dataset_labels['Stroller']
                else:
                    return -1
            elif dataset_sub == 'Mobility':
                if current_id == '0':
                    return self.dataset_labels['Bicycle']
                elif current_id == '1':
                    return self.dataset_labels['Blind']
                elif current_id == '2':
                    return self.dataset_labels['Blind']
                elif current_id == '4':
                    return self.dataset_labels['Wheelchair']
                else:
                    return -1
            elif dataset_sub == 'MobilityDetection':
                if current_id == '0':
                    return self.dataset_labels['Bicycle']
                elif current_id == '1':
                    return self.dataset_labels['Blind']
                elif current_id == '2':
                    return self.dataset_labels['Blind']
                elif current_id == '4':
                    return self.dataset_labels['Wheelchair']
                else:
                    return -1
            elif dataset_sub == 'BikeOnly':
                if current_id == '0':
                    return self.dataset_labels['Bicycle']
                else:
                    return -1
            elif dataset_sub == 'BicycleSet':
                if current_id == '0':
                    return self.dataset_labels['Bicycle']
                else:
                    return -1
            elif dataset_sub == 'ElectricScooter':
                if current_id == '0':
                    return self.dataset_labels['Scooter']
                else:
                    return -1
            elif dataset_sub == 'ElectricScooter2':
                if current_id == '0':
                    return self.dataset_labels['Scooter']
                else:
                    return -1
        